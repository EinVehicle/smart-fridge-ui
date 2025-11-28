CREATE DATABASE IF NOT EXISTS smart_fridge
  DEFAULT CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

USE smart_fridge;

CREATE TABLE IF NOT EXISTS videos (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    filename VARCHAR(255) NOT NULL,
    thumbnail VARCHAR(255),
    upload_time TIMESTAMP NULL DEFAULT NULL,
    uploaded_by VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS ai_analysis (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    item_name VARCHAR(255) NOT NULL,
    quantity INT NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    items_detected TEXT  -- JSON string of detected items
);

CREATE TABLE IF NOT EXISTS fridge_overview (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    sensor_status VARCHAR(50) DEFAULT 'offline',
    power_status VARCHAR(50) DEFAULT 'offline',
    door_open TINYINT(1) DEFAULT 0,
    free_space INT DEFAULT 0,
    last_update TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

INSERT INTO fridge_overview (sensor_status, power_statusa, door_open, free_space)
VALUES ('online', 'online', 0, 73);
