--creating a tabled named users
CREATE TABLE IF NOT EXISTS users(
  id INT AUTO_INCREMENT PRIMARY KEY NOT NULL,
  email VARCHAR(255) UNIQUE,
  name VARCHAR(255)
);
