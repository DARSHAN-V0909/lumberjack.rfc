/*
* Make sure to create this DB in your mysql workbench shell by running all the below commands before running your app
*/

CREATE DATABASE inventory_db;
USE inventory_db;
CREATE TABLE users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL
);

CREATE TABLE raw_materials (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    unit VARCHAR(20),
    current_stock INT DEFAULT 0,
    threshold INT DEFAULT 0,
    user_id INT,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE TABLE transactions (
    id INT PRIMARY KEY AUTO_INCREMENT,
    material_id INT,
    quantity INT,
    type ENUM('add', 'remove') NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    user_id INT,
    FOREIGN KEY (material_id) REFERENCES raw_materials(id),
    FOREIGN KEY (user_id) REFERENCES users(id)
);
