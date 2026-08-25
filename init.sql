-- PostgreSQL schema translated from the original Oracle SQL design
-- This file is mounted into /docker-entrypoint-initdb.d/ for automatic initialization.

CREATE TABLE restaurant_branch (
    b_number SERIAL PRIMARY KEY,
    city VARCHAR(20),
    street VARCHAR(20),
    zip_code VARCHAR(20),
    email VARCHAR(100),
    phone VARCHAR(15)
);

CREATE TABLE dish (
    name VARCHAR(30) PRIMARY KEY,
    price NUMERIC(10, 2),
    recipe VARCHAR(50),
    food_allergy VARCHAR(50),
    serving_time VARCHAR(50)
);

CREATE TABLE person (
    id SERIAL PRIMARY KEY,
    first_name VARCHAR(15),
    middle_name VARCHAR(15),
    last_name VARCHAR(15),
    phone VARCHAR(20),
    email VARCHAR(100),
    address VARCHAR(30)
);

CREATE TABLE person_order (
    num SERIAL PRIMARY KEY,
    o_time VARCHAR(15),
    o_date VARCHAR(15),
    comments VARCHAR(50),
    person_id INTEGER,
    CONSTRAINT person_order_person_fk
        FOREIGN KEY (person_id) REFERENCES person(id)
        ON DELETE CASCADE
);

CREATE TABLE chef (
    personid INTEGER PRIMARY KEY,
    salary NUMERIC(10, 2),
    speciality VARCHAR(30),
    branchnumber INTEGER,
    chef_tutorid INTEGER,
    CONSTRAINT chef_person_fk
        FOREIGN KEY (personid) REFERENCES person(id)
        ON DELETE CASCADE,
    CONSTRAINT chef_branch_fk
        FOREIGN KEY (branchnumber) REFERENCES restaurant_branch(b_number)
        ON DELETE CASCADE,
    CONSTRAINT chef_tutor_fk
        FOREIGN KEY (chef_tutorid) REFERENCES chef(personid)
        ON DELETE CASCADE
);

CREATE TABLE employee (
    personid INTEGER PRIMARY KEY,
    position VARCHAR(15),
    salary NUMERIC(10, 2),
    CONSTRAINT employee_person_fk
        FOREIGN KEY (personid) REFERENCES person(id)
        ON DELETE CASCADE
);

CREATE TABLE customer (
    personid INTEGER PRIMARY KEY,
    password VARCHAR(15),
    CONSTRAINT customer_person_fk
        FOREIGN KEY (personid) REFERENCES person(id)
        ON DELETE CASCADE
);

CREATE TABLE provide (
    branchnum INTEGER NOT NULL,
    dishname VARCHAR(30) NOT NULL,
    PRIMARY KEY (branchnum, dishname),
    CONSTRAINT provide_branch_fk
        FOREIGN KEY (branchnum) REFERENCES restaurant_branch(b_number)
        ON DELETE CASCADE,
    CONSTRAINT provide_dish_fk
        FOREIGN KEY (dishname) REFERENCES dish(name)
        ON DELETE CASCADE
);

CREATE TABLE cooking (
    chefid INTEGER NOT NULL,
    dishname VARCHAR(30) NOT NULL,
    PRIMARY KEY (chefid, dishname),
    CONSTRAINT cooking_chef_fk
        FOREIGN KEY (chefid) REFERENCES chef(personid)
        ON DELETE CASCADE,
    CONSTRAINT cooking_dish_fk
        FOREIGN KEY (dishname) REFERENCES dish(name)
        ON DELETE CASCADE
);

CREATE TABLE hasordercook (
    ordernum INTEGER NOT NULL,
    dishname VARCHAR(30) NOT NULL,
    PRIMARY KEY (ordernum, dishname),
    CONSTRAINT hasordercook_order_fk
        FOREIGN KEY (ordernum) REFERENCES person_order(num)
        ON DELETE CASCADE,
    CONSTRAINT hasordercook_dish_fk
        FOREIGN KEY (dishname) REFERENCES dish(name)
        ON DELETE CASCADE
);

-- Optional standards-conforming index suggestions for common lookup paths
CREATE INDEX idx_person_order_person_id ON person_order(person_id);
CREATE INDEX idx_chef_branch_number ON chef(branchnumber);
CREATE INDEX idx_chef_tutor_id ON chef(chef_tutorid);
CREATE INDEX idx_provide_dish_name ON provide(dishname);
CREATE INDEX idx_cooking_dish_name ON cooking(dishname);
CREATE INDEX idx_hasordercook_dish_name ON hasordercook(dishname);
