const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');

const root = path.resolve(__dirname, '..');
const html = fs.readFileSync(path.join(root, 'BelleCroissantLyonnais_Dashboard.html'), 'utf8');
const scripts = [...html.matchAll(/<script>([\s\S]*?)<\/script>/g)];
const pages = ['feedback', 'social', 'website', 'loyalty'].map(id => makeElement(id));
const buttons = pages.map((_, index) => makeElement(`button-${index}`));
pages[0].classList.add('active');
buttons[0].classList.add('active');
const elements = new Map(pages.map(element => [element.id, element]));
const plots = [];

function makeElement(id) {
  const active = new Set();
  return {
    id,
    textContent: '',
    classList: {
      add(name) { active.add(name); },
      remove(name) { active.delete(name); },
      contains(name) { return active.has(name); },
    },
  };
}

const context = {
  window: {dispatchEvent() {}},
  document: {
    getElementById(id) {
      if (!elements.has(id)) elements.set(id, makeElement(id));
      return elements.get(id);
    },
    querySelectorAll(selector) {
      return selector === '.page' ? pages : buttons;
    },
  },
  Plotly: {newPlot(id, traces) { plots.push({id, traces}); }},
  requestAnimationFrame(callback) { callback(); },
  Event: class Event {},
};
vm.createContext(context);
vm.runInContext(fs.readFileSync(path.join(root, 'dashboard-data.js'), 'utf8'), context);
vm.runInContext(scripts.at(-1)[1], context);

assert.equal(context.window.dashboardData.feedback.count, 30);
assert.deepEqual(Array.from(context.window.dashboardData.feedback.ratings), [4, 4, 3, 7, 12]);
assert.equal(context.window.dashboardData.social.likes, 4861);
assert.equal(context.window.dashboardData.social.engagement, 6391);
assert.equal(plots.length, 8);
assert.equal(new Set(plots.map(plot => plot.id)).size, 8);

context.showPage('social', buttons[1]);
assert.equal(pages[0].classList.contains('active'), false);
assert.equal(pages[1].classList.contains('active'), true);
assert.equal(buttons[1].classList.contains('active'), true);
console.log('Dashboard data and navigation checks passed');
