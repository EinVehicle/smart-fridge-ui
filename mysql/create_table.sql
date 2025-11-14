CREATE DATABASE IF NOT EXISTS smart_fridge;
USE smart_fridge;
CREATE TABLE IF NOT EXISTS fridge_overview (
    id INT AUTO_INCREMENT PRIMARY KEY,
    sensor_status ENUM('online', 'offline') NOT NULL,
    power_status ENUM('online', 'offline') NOT NULL,
    free_space INT NOT NULL,          -- 剩余空间数量
    last_update TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE IF NOT EXISTS videos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    filename VARCHAR(255) NOT NULL,   -- 存储视频文件名
    thumbnail VARCHAR(255),           -- 缩略图文件名
    upload_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE IF NOT EXISTS ai_analysis (
    id INT AUTO_INCREMENT PRIMARY KEY,
    item_name VARCHAR(255) NOT NULL,
    quantity INT NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
