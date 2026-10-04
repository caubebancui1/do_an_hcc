<<<<<<< HEAD
-- Database schema for UniTrack student management
-- Run this file in MySQL Workbench or VS Code MySQL extension.

CREATE DATABASE IF NOT EXISTS student_db
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

USE student_db;

CREATE TABLE IF NOT EXISTS accounts (
    id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    pass VARCHAR(255) NOT NULL,
    INDEX idx_accounts_username (username)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS students (
    id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    student_code VARCHAR(20) NOT NULL UNIQUE,
    full_name VARCHAR(120) NOT NULL,
    email VARCHAR(160) NOT NULL UNIQUE,
    phone VARCHAR(20),
    date_of_birth DATE,
    gender ENUM('Nam', 'Nữ', 'Khác') NOT NULL DEFAULT 'Khác',
    major VARCHAR(120) NOT NULL,
    class_name VARCHAR(50) NOT NULL,
    dtb DECIMAL(3, 2) NOT NULL DEFAULT 0.00,
    status ENUM('Đang học', 'Bảo lưu', 'Đã tốt nghiệp') NOT NULL DEFAULT 'Đang học',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_students_major (major),
    INDEX idx_students_status (status)
) ENGINE=InnoDB;

INSERT INTO accounts (username, pass)
VALUES ('admin', '$2b$12$3Yk7n5vP2ZP3LNR8f8yV5uN2G2mR3W8lpp4hKxM9wJxk1P0a1eQ2e')
ON DUPLICATE KEY UPDATE
    pass = VALUES(pass);

INSERT INTO students
    (student_code, full_name, email, phone, date_of_birth, gender, major, class_name, dtb, status)
VALUES
    ('SV2024001', 'Nguyễn Minh Anh', 'minhanh@university.edu.vn', '0901234567', '2005-04-12', 'Nữ', 'Công nghệ thông tin', 'K18A1', 3.72, 'Đang học'),
    ('SV2024002', 'Trần Quốc Bảo', 'quocbao@university.edu.vn', '0912345678', '2004-11-23', 'Nam', 'Kinh doanh quốc tế', 'K18KD2', 3.45, 'Đang học'),
    ('SV2023008', 'Lê Hoàng Nam', 'hoangnam@university.edu.vn', '0987654321', '2003-08-09', 'Nam', 'Thiết kế đồ họa', 'K17TK1', 3.18, 'Bảo lưu')
ON DUPLICATE KEY UPDATE
    full_name = VALUES(full_name),
    email = VALUES(email),
    phone = VALUES(phone),
    major = VALUES(major),
    class_name = VALUES(class_name),
    dtb = VALUES(dtb),
    status = VALUES(status);

SELECT * FROM accounts;
SELECT * FROM students ORDER BY created_at DESC;
=======
-- Database schema for UniTrack student management
-- Run this file in MySQL Workbench or VS Code MySQL extension.

CREATE DATABASE IF NOT EXISTS student_db
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

USE student_db;

CREATE TABLE IF NOT EXISTS accounts (
    id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    pass VARCHAR(255) NOT NULL,
    INDEX idx_accounts_username (username)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS students (
    id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    student_code VARCHAR(20) NOT NULL UNIQUE,
    full_name VARCHAR(120) NOT NULL,
    email VARCHAR(160) NOT NULL UNIQUE,
    phone VARCHAR(20),
    date_of_birth DATE,
    gender ENUM('Nam', 'Nữ', 'Khác') NOT NULL DEFAULT 'Khác',
    major VARCHAR(120) NOT NULL,
    class_name VARCHAR(50) NOT NULL,
    dtb DECIMAL(3, 2) NOT NULL DEFAULT 0.00,
    status ENUM('Đang học', 'Bảo lưu', 'Đã tốt nghiệp') NOT NULL DEFAULT 'Đang học',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_students_major (major),
    INDEX idx_students_status (status)
) ENGINE=InnoDB;

INSERT INTO accounts (username, pass)
VALUES ('admin', '$2b$12$3Yk7n5vP2ZP3LNR8f8yV5uN2G2mR3W8lpp4hKxM9wJxk1P0a1eQ2e')
ON DUPLICATE KEY UPDATE
    pass = VALUES(pass);

INSERT INTO students
    (student_code, full_name, email, phone, date_of_birth, gender, major, class_name, dtb, status)
VALUES
    ('SV2024001', 'Nguyễn Minh Anh', 'minhanh@university.edu.vn', '0901234567', '2005-04-12', 'Nữ', 'Công nghệ thông tin', 'K18A1', 3.72, 'Đang học'),
    ('SV2024002', 'Trần Quốc Bảo', 'quocbao@university.edu.vn', '0912345678', '2004-11-23', 'Nam', 'Kinh doanh quốc tế', 'K18KD2', 3.45, 'Đang học'),
    ('SV2023008', 'Lê Hoàng Nam', 'hoangnam@university.edu.vn', '0987654321', '2003-08-09', 'Nam', 'Thiết kế đồ họa', 'K17TK1', 3.18, 'Bảo lưu')
ON DUPLICATE KEY UPDATE
    full_name = VALUES(full_name),
    email = VALUES(email),
    phone = VALUES(phone),
    major = VALUES(major),
    class_name = VALUES(class_name),
    dtb = VALUES(dtb),
    status = VALUES(status);

SELECT * FROM accounts;
SELECT * FROM students ORDER BY created_at DESC;
>>>>>>> 20e273270e4e56e8663036fc5b11e7151b128a20
