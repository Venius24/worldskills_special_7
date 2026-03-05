-- Belle Croissant Lyonnais BI Database Schema
-- WorldSkills Competition 2024 - Session 7

CREATE DATABASE IF NOT EXISTS BelleCroissantLyonnaisBI;
USE BelleCroissantLyonnaisBI;

DROP TABLE IF EXISTS LoyaltyProgramHistory;
DROP TABLE IF EXISTS WebsiteAnalytics;
DROP TABLE IF EXISTS SocialMediaEngagement;
DROP TABLE IF EXISTS CustomerFeedback;
DROP TABLE IF EXISTS Customers;

CREATE TABLE Customers (
    CustomerID INT PRIMARY KEY,
    Name VARCHAR(255) NOT NULL,
    Email VARCHAR(255) NOT NULL UNIQUE,
    JoinDate DATE NOT NULL,
    City VARCHAR(100),
    Country VARCHAR(100)
);

CREATE TABLE CustomerFeedback (
    FeedbackID INT PRIMARY KEY,
    CustomerID INT NOT NULL,
    Date DATE NOT NULL,
    Rating INT NOT NULL CHECK (Rating >= 1 AND Rating <= 5),
    Comments TEXT,
    FOREIGN KEY (CustomerID) REFERENCES Customers(CustomerID)
);

CREATE TABLE SocialMediaEngagement (
    PostID INT PRIMARY KEY,
    Platform VARCHAR(50) NOT NULL,
    Date DATE NOT NULL,
    Likes INT DEFAULT 0,
    Shares INT DEFAULT 0,
    Comments INT DEFAULT 0,
    PostType VARCHAR(50)
);

CREATE TABLE WebsiteAnalytics (
    AnalyticsID INT PRIMARY KEY,
    Date DATE NOT NULL,
    Page VARCHAR(255) NOT NULL,
    Pageviews INT DEFAULT 0,
    UniqueVisitors INT DEFAULT 0,
    AverageTimeOnPage INT DEFAULT 0
);

CREATE TABLE LoyaltyProgramHistory (
    TransactionID INT PRIMARY KEY,
    CustomerID INT NOT NULL,
    TransactionDate DATE NOT NULL,
    ActionType VARCHAR(50) NOT NULL,
    PointsEarned INT DEFAULT 0,
    PointsRedeemed INT DEFAULT 0,
    PointsBalance INT DEFAULT 0,
    FOREIGN KEY (CustomerID) REFERENCES Customers(CustomerID)
);

CREATE INDEX idx_customer_feedback_date ON CustomerFeedback(Date);
CREATE INDEX idx_social_media_date ON SocialMediaEngagement(Date);
CREATE INDEX idx_website_date ON WebsiteAnalytics(Date);
CREATE INDEX idx_loyalty_date ON LoyaltyProgramHistory(TransactionDate);
