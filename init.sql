CREATE TABLE IF NOT EXISTS contacts (
    id SERIAL PRIMARY KEY,
    full_name VARCHAR(255) NOT NULL,
    phone_number VARCHAR(20) NOT NULL,
    note TEXT
);

INSERT INTO contacts (full_name, phone_number, note)
VALUES ('Иванов Иван Иванович', '89002756336', 'первый контакт')