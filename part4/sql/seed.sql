-- Insert Administrator User
INSERT INTO users (id, first_name, last_name, email, password, is_admin)
VALUES (
    '36c9050e-ddd3-4c3b-9731-9f487208bbc1',
    'Admin',
    'HBnB',
    'admin@hbnb.io',
    '$2b$12$K1vGj3wE4C/oA3J37wW6u.E6YlWwGj6A9H3YyO0O0k8wQ0/aW9Zym',
    TRUE
);

-- Insert Initial Amenities
INSERT INTO amenities (id, name)
VALUES 
    ('7d3e9c1a-5b4f-4e2d-8a3c-1b9f6d7e4a2b', 'WiFi'),
    ('9f2b8c4d-1e3a-4f5b-6c7d-8e9f0a1b2c3d', 'Swimming Pool'),
    ('3a5c7e9f-2b4d-4f1a-8c3e-6d9f1a2b4c5e', 'Air Conditioning');
