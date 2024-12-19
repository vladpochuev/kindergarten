CREATE DATABASE kindergarten;

\c kindergarten;

CREATE TABLE menu (
    id SERIAL PRIMARY KEY,
    since DATE,
    name VARCHAR(20),
    description TEXT
);

CREATE TABLE parents (
    id SERIAL PRIMARY KEY,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    birth_date DATE,
    phone VARCHAR(20),
    email VARCHAR(50),
    gender VARCHAR(10),
    hash_password VARCHAR(256)
);

CREATE TABLE educators (
    id SERIAL PRIMARY KEY,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    birth_date DATE,
    phone VARCHAR(20),
    email VARCHAR(50),
    qualification VARCHAR(50),
    gender VARCHAR(10)
);

CREATE TABLE groups (
    id SERIAL PRIMARY KEY,
    educator_id INT,
    name VARCHAR(50),
    from_age INT,
    to_age INT,
    FOREIGN KEY (educator_id) REFERENCES educators(id)
);

CREATE TABLE children (
    id SERIAL PRIMARY KEY,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    birth_date DATE,
    gender VARCHAR(10),
    group_id INT,
    parent_id INT,
    menu_id INT,
    FOREIGN KEY (group_id) REFERENCES groups(id),
    FOREIGN KEY (parent_id) REFERENCES parents(id),
    FOREIGN KEY (menu_id) REFERENCES menu(id)
);

ALTER TABLE children
ADD CONSTRAINT check_child_age
CHECK (EXTRACT(YEAR FROM AGE(birth_date)) >= 0 AND EXTRACT(YEAR FROM AGE(birth_date)) <= 7);