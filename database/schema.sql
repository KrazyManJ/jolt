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

