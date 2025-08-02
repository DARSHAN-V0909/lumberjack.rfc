/*
* Make sure to create this DB in your mysql workbench shell by running all the below commands before running your app
* What is the  use of this file?
* In case  you want to run the program and also have the data of a few users you can use this, just go to your MySQl workbench and
* run whatever queries you havent run already and your DB should be synced with all the collaborators.
* THIS WILL BE REMOVED ON PROD
*/

CREATE DATABASE inventory_db;
USE inventory_db;
CREATE TABLE users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL
);

CREATE TABLE raw_materials (
    material_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL UNIQUE,
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
    FOREIGN KEY (material_id) REFERENCES raw_materials(material_id),
    FOREIGN KEY (user_id) REFERENCES users(id)
);
INSERT INTO users (username, password_hash) VALUES ('vishnu', 'password');
INSERT INTO raw_materials (name, unit, current_stock, threshold, user_id) VALUES ('Rice', 'kg', 100, 10, 1);
INSERT INTO raw_materials (name, unit, current_stock, threshold, user_id) VALUES ('Cement', 'kg', 20, 5, 1);
INSERT INTO users (username, password_hash) VALUES ('person', 'tangela');
INSERT INTO raw_materials (name, unit, current_stock, threshold, user_id) VALUES ('Cotton', 'bags', 10, 1, 2);
INSERT INTO raw_materials (name, unit, current_stock, threshold, user_id) VALUES ('Cheese', 'kg', 20, 7, 2);
INSERT INTO raw_materials (name, unit, current_stock, threshold, user_id) VALUES ('Vineager', 'Liters', 200, 70, 2);
