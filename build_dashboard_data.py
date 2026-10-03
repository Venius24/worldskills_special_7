"""Build the dashboard's browser-ready snapshot from the five local CSV files."""

import argparse
import csv
import json
from collections import Counter, defaultdict
from datetime import date
from pathlib import Path


ROOT = Path(__file__).resolve().parent
DATA_DIR = ROOT / 'belle_croissant_bi' / 'data'
OUTPUT = ROOT / 'dashboard-data.js'


def read_rows(name):
    with (DATA_DIR / name).open(encoding='utf-8-sig', newline='') as source:
        return list(csv.DictReader(source))


def snapshot():
    feedback = read_rows('customer_feedback.csv')
    social = read_rows('social_media_engagement.csv')
    website = read_rows('website_analytics.csv')
    loyalty = read_rows('loyalty_program_history.csv')
    customers = read_rows('customers_data.csv')
    customer_ids = {int(row['CustomerID']) for row in customers}
    if len(customer_ids) != len(customers):
        raise ValueError('Duplicate CustomerID in customers_data.csv')
    for row in feedback + loyalty:
        if int(row['CustomerID']) not in customer_ids:
            raise ValueError('Feedback or loyalty row references an unknown customer')

    ratings = Counter(int(row['Rating']) for row in feedback)
    weekly = defaultdict(list)
    for row in feedback:
        year, week, _ = date.fromisoformat(row['Date']).isocalendar()
        weekly[f'{year}-W{week:02d}'].append(int(row['Rating']))
    weeks = sorted(weekly)

    platforms = defaultdict(lambda: {'likes': 0, 'shares': 0, 'comments': 0})
    for row in social:
        values = platforms[row['Platform']]
        for column, key in [('Likes', 'likes'), ('Shares', 'shares'), ('Comments', 'comments')]:
            values[key] += int(row[column])
    platform_names = sorted(platforms)

    pages = Counter()
    for row in website:
        pages[row['Page']] += int(row['Pageviews'])
    top_pages = pages.most_common(5)

    latest_balance = {}
    actions = Counter()
    for row in loyalty:
        customer_id = int(row['CustomerID'])
        key = (date.fromisoformat(row['TransactionDate']), int(row['TransactionID']))
        if customer_id not in latest_balance or key > latest_balance[customer_id][0]:
            latest_balance[customer_id] = (key, int(row['PointsBalance']))
        actions[row['ActionType']] += 1
    top_customers = sorted(
        ((customer_id, result[1]) for customer_id, result in latest_balance.items()),
        key=lambda item: (-item[1], item[0]),
    )[:5]

    return {
        'feedback': {
            'count': len(feedback),
            'average': round(sum(rating * count for rating, count in ratings.items()) / len(feedback), 2),
            'positive_pct': round(100 * sum(count for rating, count in ratings.items() if rating >= 4) / len(feedback)),
            'weeks': weeks,
            'weekly_average': [round(sum(weekly[week]) / len(weekly[week]), 2) for week in weeks],
            'weekly_count': [len(weekly[week]) for week in weeks],
            'ratings': [ratings[rating] for rating in range(1, 6)],
            'sentiment': [sum(ratings[r] for r in (4, 5)), sum(ratings[r] for r in (1, 2)), ratings[3]],
        },
        'social': {
            'posts': len(social),
            'likes': sum(values['likes'] for values in platforms.values()),
            'engagement': sum(sum(values.values()) for values in platforms.values()),
            'platforms': platform_names,
            'likes_by_platform': [platforms[name]['likes'] for name in platform_names],
            'shares_by_platform': [platforms[name]['shares'] for name in platform_names],
            'comments_by_platform': [platforms[name]['comments'] for name in platform_names],
        },
        'website': {
            'pageviews': sum(pages.values()),
            'unique_visitors_sum': sum(int(row['UniqueVisitors']) for row in website),
            'top_pages': [name for name, _ in top_pages],
            'top_pageviews': [count for _, count in top_pages],
        },
        'loyalty': {
            'customers_total': len(customers),
            'members': len(latest_balance),
            'average_balance': round(sum(balance for _, balance in latest_balance.values()) / len(latest_balance), 2),
            'top_customers': [f'Клиент #{customer_id}' for customer_id, _ in top_customers],
            'top_balances': [balance for _, balance in top_customers],
            'actions': [action for action, _ in actions.most_common()],
            'action_counts': [count for _, count in actions.most_common()],
        },
    }


def render():
    return 'window.dashboardData = ' + json.dumps(snapshot(), ensure_ascii=False, separators=(',', ':')) + ';\n'


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true', help='verify dashboard-data.js is up to date')
    args = parser.parse_args()
    content = render()
    if args.check:
        if not OUTPUT.exists() or OUTPUT.read_text(encoding='utf-8') != content:
            raise SystemExit('dashboard-data.js is out of date; run build_dashboard_data.py')
        print('dashboard-data.js matches CSV sources')
    else:
        OUTPUT.write_text(content, encoding='utf-8')
        print('Updated dashboard-data.js from CSV sources')
