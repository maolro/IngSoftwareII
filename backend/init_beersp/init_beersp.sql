-- CONNECT: docker exec -it beersp-db mysql -u root -p
USE beersp_db;

-- Create users table with MySQL syntax
CREATE TABLE IF NOT EXISTS users (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    birth_date DATE,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Create user_friends table with proper MySQL foreign key syntax
CREATE TABLE IF NOT EXISTS user_friends (
    user_id BIGINT,
    friend_id BIGINT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (user_id, friend_id),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (friend_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Insert sample data with MySQL syntax (no ON CONFLICT in MySQL)
INSERT IGNORE INTO users (username, email, birth_date, password_hash) VALUES
('john_doe', 'john@example.com', '1990-05-15', 'hashed_password_123'),
('jane_smith', 'jane@example.com', '1992-08-20', 'hashed_password_456'),
('beer_lover', 'beer@example.com', '1988-12-01', 'hashed_password_789');

-- Insert friend relationships
INSERT IGNORE INTO user_friends (user_id, friend_id) VALUES
(1, 2), (1, 3), (2, 1);