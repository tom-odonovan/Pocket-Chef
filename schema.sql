DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS favourites;

CREATE TABLE users(
    id SERIAL PRIMARY KEY,
    email TEXT,
    given_name TEXT,
    surname TEXT,
    password_hash TEXT,
    admin BOOLEAN
);

CREATE TABLE favourites(
    id SERIAL PRIMARY KEY,
    user_id INTEGER,
    recipe_id INTEGER,

    FOREIGN KEY (user_id)
        REFERENCES users(id)
)

CREATE TABLE shopping_list(
    id SERIAL PRIMARY KEY,
    user_id INTEGER,
    quantity INTEGER,
    ingredient INTEGER,

    FOREIGN KEY (user_id)
        REFERENCES users(id)
)
