USE inventory_db;

INSERT INTO purchases (product_name, quantity, buyer_name) VALUES
    ('Wireless Mouse', 2, 'Daniel'),
    ('USB-C Cable', 5, 'Sarah'),
    ('Laptop Stand', 1, 'Michael'),
    ('Mechanical Keyboard', 1, 'Aylin');

SELECT id, product_name, quantity, buyer_name, created_at
FROM purchases
ORDER BY id;
