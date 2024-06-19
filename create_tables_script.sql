DROP DATABASE IF EXISTS fig;
CREATE DATABASE fig;
USE fig;

CREATE TABLE fig_category (
	fig_category_id INT NOT NULL AUTO_INCREMENT,
    name VARCHAR(250),
	PRIMARY KEY (fig_category_id)
);
-- select * from fig_category;

CREATE TABLE menu_category (
	menu_category_id INT NOT NULL AUTO_INCREMENT,
    name VARCHAR(250),
	PRIMARY KEY (menu_category_id)
);
-- select * from menu_category;

CREATE TABLE restaurant (
	restaurant_id INT NOT NULL AUTO_INCREMENT,
    name VARCHAR(250),
	PRIMARY KEY (restaurant_id)
);
-- select * from restaurant;

CREATE TABLE menu_item (
	menu_item_id INT NOT NULL AUTO_INCREMENT,
    name VARCHAR(250),
    ingredients VARCHAR(10000),
    allergens VARCHAR(1000),
    picture_url VARCHAR(10000),
    restaurant_id INT,
    menu_category_id INT,
    fig_category_id INT,
	PRIMARY KEY (menu_item_id),
    FOREIGN KEY (restaurant_id) REFERENCES restaurant(restaurant_id),
    FOREIGN KEY (menu_category_id) REFERENCES menu_category(menu_category_id),
    FOREIGN KEY (fig_category_id) REFERENCES fig_category(fig_category_id)
);
-- select * from menu_item;
