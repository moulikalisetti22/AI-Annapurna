CREATE DATABASE IF NOT EXISTS foodbridge;
USE foodbridge;

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    full_name VARCHAR(120) NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role ENUM('donor','ngo','volunteer','admin') NOT NULL,
    phone VARCHAR(20),
    village VARCHAR(120),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE donations (
    id INT AUTO_INCREMENT PRIMARY KEY,
    donor_id INT NOT NULL,
    food_name VARCHAR(120) NOT NULL,
    quantity VARCHAR(50) NOT NULL,
    food_type VARCHAR(50) NOT NULL,
    location VARCHAR(150) NOT NULL,
    latitude DECIMAL(9,6) NOT NULL,
    longitude DECIMAL(9,6) NOT NULL,
    pickup_time VARCHAR(100) NOT NULL,
    expiry_time DATETIME NOT NULL,
    safety_note TEXT,
    image_url VARCHAR(255),
    status ENUM('Available','Accepted','Picked Up','Delivered') DEFAULT 'Available',
    is_demo BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (donor_id) REFERENCES users(id)
);

CREATE TABLE requests (
    id INT AUTO_INCREMENT PRIMARY KEY,
    donation_id INT NOT NULL,
    requester_id INT NOT NULL,
    request_type ENUM('ngo','recipient') DEFAULT 'ngo',
    status ENUM('Pending','Accepted','Picked Up','Delivered') DEFAULT 'Pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (donation_id) REFERENCES donations(id),
    FOREIGN KEY (requester_id) REFERENCES users(id)
);

CREATE TABLE tasks (
    id INT AUTO_INCREMENT PRIMARY KEY,
    volunteer_id INT NOT NULL,
    donation_id INT NOT NULL,
    pickup_location VARCHAR(150) NOT NULL,
    drop_location VARCHAR(150) NOT NULL,
    task_status ENUM('Assigned','In Transit','Completed') DEFAULT 'Assigned',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (volunteer_id) REFERENCES users(id),
    FOREIGN KEY (donation_id) REFERENCES donations(id)
);

CREATE TABLE notifications (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    message TEXT NOT NULL,
    type VARCHAR(50) DEFAULT 'info',
    is_read BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

INSERT INTO users (full_name, email, password_hash, role, phone, village)
VALUES
('Asha Donor', 'donor@foodbridge.in', '$2b$12$9k2L1bq3d0jEG6Q5x9fpFea0fY5nQkJr1i42p6T5HrH7OWrWjE9em', 'donor', '9876543210', 'Konduru'),
('Green Hope NGO', 'ngo@foodbridge.in', '$2b$12$9k2L1bq3d0jEG6Q5x9fpFea0fY5nQkJr1i42p6T5HrH7OWrWjE9em', 'ngo', '9123456780', 'Peddapalli'),
('Ravi Volunteer', 'volunteer@foodbridge.in', '$2b$12$9k2L1bq3d0jEG6Q5x9fpFea0fY5nQkJr1i42p6T5HrH7OWrWjE9em', 'volunteer', '9988776655', 'Sattenapalli'),
('Admin User', 'admin@foodbridge.in', '$2b$12$9k2L1bq3d0jEG6Q5x9fpFea0fY5nQkJr1i42p6T5HrH7OWrWjE9em', 'admin', '9000000000', 'Head Office');

INSERT INTO donations (donor_id, food_name, quantity, food_type, location, latitude, longitude, pickup_time, expiry_time, safety_note, image_url, status, is_demo)
VALUES
(1, 'Rice and Curry', '18 plates', 'Cooked Meal', 'Konduru Market', 16.6230, 80.2000, '18:30 Today', DATE_ADD(NOW(), INTERVAL 6 HOUR), 'Prepared within 4 hours; kept covered and sealed', '/static/uploads/demo-rice.jpg', 'Available', TRUE),
(1, 'Vegetable Biryani', '25 servings', 'Cooked Meal', 'Mangalagiri Road', 16.4300, 80.5400, 'Tomorrow 9:00 AM', DATE_ADD(NOW(), INTERVAL 12 HOUR), 'Freshly cooked; no dairy added', '/static/uploads/demo-biryani.jpg', 'Accepted', TRUE),
(1, 'Fresh Bread', '30 loaves', 'Bakery', 'Nallapadu Junction', 16.3100, 80.4300, 'Today 18:00', DATE_ADD(NOW(), INTERVAL 2 DAY), 'Stored in hygienic conditions', '/static/uploads/demo-bread.jpg', 'Available', TRUE);

INSERT INTO requests (donation_id, requester_id, request_type, status)
VALUES
(2, 2, 'ngo', 'Accepted'),
(3, 2, 'ngo', 'Pending');

INSERT INTO tasks (volunteer_id, donation_id, pickup_location, drop_location, task_status)
VALUES
(3, 2, 'Mangalagiri Road', 'Green Hope NGO Center', 'In Transit'),
(3, 3, 'Nallapadu Junction', 'Vulnerable Family Shelter', 'Assigned');

INSERT INTO notifications (user_id, message, type, is_read)
VALUES
(1, 'Your donation at Konduru Market has been accepted by Green Hope NGO.', 'status', FALSE),
(3, 'New pickup assigned for bread donation from Nallapadu Junction.', 'task', FALSE);
