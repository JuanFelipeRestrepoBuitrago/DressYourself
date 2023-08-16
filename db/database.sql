DROP SCHEMA IF EXISTS dress_your_self;
CREATE SCHEMA dress_your_self DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci;

USE dress_your_self;

DROP TABLE IF EXISTS dress_your_self.users;
CREATE TABLE dress_your_self.users (
    id INT UNSIGNED NOT NULL AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL,
    username VARCHAR(100) DEFAULT NULL,
    password VARCHAR(100) NOT NULL,
    PRIMARY KEY (id),
    UNIQUE INDEX email_UNIQUE (email ASC),
    UNIQUE INDEX username_UNIQUE (username ASC)
);

DROP TABLE IF EXISTS dress_your_self.clothes;
CREATE TABLE dress_your_self.clothes (
    id INT UNSIGNED NOT NULL AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    description VARCHAR(500) NOT NULL,
    image 
);


