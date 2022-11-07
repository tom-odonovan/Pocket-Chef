DROP TABLE IF EXISTS users;

CREATE TABLE users(
    id SERIAL PRIMARY KEY,
    email TEXT,
    given_name TEXT,
    surname TEXT,
    password_hash TEXT,
    admin BOOLEAN
);