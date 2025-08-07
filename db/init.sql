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
CREATE TABLE suppliers(
    supplier_id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT,
    material_id INT,
    supplier_name VARCHAR(200),
    phone_number VARCHAR(15),
    FOREIGN KEY (material_id) REFERENCES raw_materials(material_id),
    FOREIGN KEY (user_id) REFERENCES users(id)
);
CREATE TABLE menu_items(
    menu_id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT,
    item_name VARCHAR(50),
    FOREIGN KEY(user_id) REFERENCES users(id)
);
CREATE TABLE menu_requirements(
    user_id INT,
    menu_id INT ,
    material_id INT ,
    PRIMARY KEY (user_id, menu_id, material_id),
    FOREIGN KEY(user_id) REFERENCES menu_items(user_id),
    FOREIGN KEY(menu_id) REFERENCES menu_items(menu_id),
    FOREIGN KEY(material_id) REFERENCES raw_materials(material_id)
);
