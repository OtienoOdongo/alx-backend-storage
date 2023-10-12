--creating an sql script for TABLE
--the name of the table is users
CREATE TABLE IF NOT EXISTS users(
  id INT AUTO_INCREMENT PRIMARY KEY NOT NULL,
  email VARCHAR(255) NOT NULL UNIQUE,
  name VARCHAR(255)
);
