DROP TABLE IF EXISTS users;

DROP TABLE IF EXISTS roles;

CREATE TABLE roles (
    role_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL
);

INSERT INTO roles (name) VALUES ('user'),('employee'),('admin');

CREATE TABLE users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    role_id INTEGER DEFAULT 1 NOT NULL,
    login_name TEXT NOT NULL,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    password_hash TEXT NOT NULL,
    email TEXT NOT NULL,
    phone_number TEXT NOT NULL,
    is_deactivated INTEGER DEFAULT 0 NOT NULL,
    FOREIGN KEY (role_id) REFERENCES roles (role_id)
);

CREATE TABLE bikes (
    bike_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    description TEXT NULL,
    weight INTEGER NOT NULL,
    body_size TEXT NOT NULL,
    wheel_size TEXT NOT NULL,
    body_material TEXT NOT NULL,
    gear_number INTEGER NOT NULL,
    weight_limit INTEGER NOT NULL,
    is_available INTEGER DEFAULT 1 NOT NULL,
    is_shown INTEGER DEFAULT 1 NOT NULL
);