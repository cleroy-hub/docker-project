CREATE DATABASE IF NOT EXISTS docker_project;
USE docker_project;
CREATE TABLE user ( id INT PRIMARY KEY NOT NULL AUTO_INCREMENT, name VARCHAR(255), mail VARCHAR(255), password VARCHAR(255));
INSERT INTO user VALUES ('celine', 'celine@gmail.com', 'leroy');
INSERT INTO user VALUES ('brad', 'brad@gmail.com', 'pitt');
INSERT INTO user VALUES ('jack', 'jack@gmail.com', 'sparrow');