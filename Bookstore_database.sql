create database bookstore;
use bookstore;

-- Customers Table
CREATE TABLE customers (
    customer_id INT AUTO_INCREMENT PRIMARY KEY,
    c_name VARCHAR(50),
    email VARCHAR(50),
    phone VARCHAR(15),
    address VARCHAR(100)
);

-- Books Table
CREATE TABLE books (
    book_id INT AUTO_INCREMENT PRIMARY KEY,
    b_name VARCHAR(100),
    author VARCHAR(50),
    price DECIMAL(10,2),
    stock INT
);

-- Orders Table
CREATE TABLE orders (
    order_id INT AUTO_INCREMENT PRIMARY KEY,
    customer_id INT,
    total_amount DECIMAL(10,2),
    status VARCHAR(20) DEFAULT 'Pending',
    order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);

-- Order Items Table
CREATE TABLE order_items (
    order_item_id INT AUTO_INCREMENT PRIMARY KEY,
    order_id INT,
    book_id INT,
    quantity INT,
    item_total DECIMAL(10,2),
    FOREIGN KEY (order_id) REFERENCES orders(order_id),
    FOREIGN KEY (book_id) REFERENCES books(book_id)
);

-- Payments Table
CREATE TABLE payments (
    payment_id INT AUTO_INCREMENT PRIMARY KEY,
    order_id INT,
    method VARCHAR(20),
    amount DECIMAL(10,2),
    status VARCHAR(20) DEFAULT 'Pending',
    payment_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (order_id) REFERENCES orders(order_id)
);

INSERT INTO customers (c_name, email, phone, address) VALUES
('Aman Sharma', 'aman@gmail.com', '9876543210', 'Delhi'),
('Riya Verma', 'riya@gmail.com', '8765432109', 'Mumbai');

INSERT INTO books (b_name, author, price, stock) VALUES
('Python Programming', 'Mark Lutz', 550.00, 10),
('DBMS Concepts', 'Korth', 600.00, 8),
('Web Development', 'Jon Duckett', 700.00, 6);

DELIMITER $$
CREATE PROCEDURE place_order(
    IN p_customer_id INT,
    IN p_book_id INT,
    IN p_quantity INT
)
BEGIN
    DECLARE v_price DECIMAL(10,2);
    DECLARE v_total DECIMAL(10,2);
    DECLARE v_stock INT;
    DECLARE v_order_id INT;

    SELECT price, stock INTO v_price, v_stock FROM books WHERE book_id = p_book_id;

    IF v_stock < p_quantity THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Not enough stock available';
    ELSE
        SET v_total = v_price * p_quantity;

        INSERT INTO orders (customer_id, total_amount, status)
        VALUES (p_customer_id, v_total, 'Pending');

        SET v_order_id = LAST_INSERT_ID();

        INSERT INTO order_items (order_id, book_id, quantity, item_total)
        VALUES (v_order_id, p_book_id, p_quantity, v_total);

        UPDATE books SET stock = stock - p_quantity WHERE book_id = p_book_id;
    END IF;
END $$
DELIMITER ;

DELIMITER $$
CREATE PROCEDURE make_payment(
    IN p_order_id INT,
    IN p_method VARCHAR(20)
)
BEGIN
    DECLARE v_amount DECIMAL(10,2);

    SELECT total_amount INTO v_amount FROM orders WHERE order_id = p_order_id;

    INSERT INTO payments (order_id, method, amount, status)
    VALUES (p_order_id, p_method, v_amount, 'Paid');

    UPDATE orders SET status = 'Paid' WHERE order_id = p_order_id;
END $$
DELIMITER ;

DELIMITER $$
CREATE FUNCTION get_order_total(p_order_id INT)
RETURNS DECIMAL(12,2)
DETERMINISTIC
BEGIN
    DECLARE v_total DECIMAL(12,2);
    SELECT total_amount INTO v_total FROM orders WHERE order_id = p_order_id;
    RETURN v_total;
END $$
DELIMITER ;

CREATE OR REPLACE VIEW order_summary AS
SELECT 
    o.order_id,
    c.c_name AS customer_name,
    b.b_name AS book_title,
    oi.quantity,
    oi.item_total,
    o.total_amount,
    o.status AS order_status,
    p.status AS payment_status
FROM orders o
JOIN customers c ON o.customer_id = c.customer_id
JOIN order_items oi ON o.order_id = oi.order_id
JOIN books b ON oi.book_id = b.book_id
LEFT JOIN payments p ON o.order_id = p.order_id;

DELIMITER $$
CREATE TRIGGER check_stock_before_update
BEFORE UPDATE ON books
FOR EACH ROW
BEGIN
    IF NEW.stock < 0 THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Stock cannot be negative';
    END IF;
END $$
DELIMITER ;

-- Place an order
CALL place_order(1, 1, 2);

-- Make payment
CALL make_payment(1, 'Online');

-- Check all tables
SELECT * FROM customers;
SELECT * FROM books;
SELECT * FROM order_items;
SELECT * FROM payments;

SELECT * FROM order_summary;
