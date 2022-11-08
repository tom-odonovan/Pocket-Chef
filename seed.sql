TRUNCATE TABLE users;

ALTER SEQUENCE users_id_seq RESTART WITH 1;

INSERT INTO users (email, given_name, surname, password_hash, admin)
VALUES ('tom.odonovan01@gmail.com', 'Tom', 'ODonovan', '$2b$12$vyk4pzrAGXsQ97oVsHVAGe0SGHhZH3UqZoowYPLTxvge8NvWCBEAK', TRUE);