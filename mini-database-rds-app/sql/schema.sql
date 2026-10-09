-- Run this against your RDS MySQL instance once, before starting the app.
CREATE DATABASE IF NOT EXISTS mini_database;
USE mini_database;

CREATE TABLE IF NOT EXISTS records (
    id   INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    role VARCHAR(100),
    city VARCHAR(100)
);

-- Recommended: a dedicated least-privilege user for the app
-- (instead of the RDS master user).
-- CREATE USER 'mini_app'@'%' IDENTIFIED BY 'choose-a-strong-password';
-- GRANT SELECT, INSERT, UPDATE, DELETE ON mini_database.* TO 'mini_app'@'%';
-- FLUSH PRIVILEGES;
