-- Database Verification Script

SELECT 'Checking Customers table...' AS Status;
SELECT COUNT(*) AS RowCount FROM Customers;
SELECT * FROM Customers LIMIT 5;

SELECT 'Checking CustomerFeedback table...' AS Status;
SELECT COUNT(*) AS RowCount FROM CustomerFeedback;
SELECT * FROM CustomerFeedback LIMIT 5;

SELECT 'Checking SocialMediaEngagement table...' AS Status;
SELECT COUNT(*) AS RowCount FROM SocialMediaEngagement;
SELECT * FROM SocialMediaEngagement LIMIT 5;

SELECT 'Checking WebsiteAnalytics table...' AS Status;
SELECT COUNT(*) AS RowCount FROM WebsiteAnalytics;
SELECT * FROM WebsiteAnalytics LIMIT 5;

SELECT 'Checking LoyaltyProgramHistory table...' AS Status;
SELECT COUNT(*) AS RowCount FROM LoyaltyProgramHistory;
SELECT * FROM LoyaltyProgramHistory LIMIT 5;

SELECT 'All checks complete!' AS Status;
