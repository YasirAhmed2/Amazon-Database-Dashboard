-- Customer Table
CREATE TABLE Customer (
    customer_id INT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    phone VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP  
);

-- Customer Address Table (1-to-many)
CREATE TABLE CustomerAddress (
    address_id INT PRIMARY KEY,
    customer_id INT NOT NULL,
    address TEXT NOT NULL,
    city VARCHAR(100),
    state VARCHAR(100),
    postal_code VARCHAR(100),
    country VARCHAR(100),
    FOREIGN KEY (customer_id) REFERENCES Customer(customer_id)
);

-- Admin Table
CREATE TABLE Admin (
    admin_id INT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    user_name VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP  
);

-- Admin Login Table
CREATE TABLE AdminLogin (
    login_id INT PRIMARY KEY,
    admin_id INT NOT NULL,
    login_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (admin_id) REFERENCES Admin(admin_id)
);

-- Customer Login Table
CREATE TABLE CustomerLogin (
    login_id INT PRIMARY KEY,
    customer_id INT NOT NULL,
    login_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (customer_id) REFERENCES Customer(customer_id)
);

-- Supplier Table
CREATE TABLE Supplier (
    supplier_id INT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    phone VARCHAR(100)
);

-- Category Table
CREATE TABLE Category (
    category_id INT PRIMARY KEY,
    category_name VARCHAR(100) NOT NULL
);

-- Product Table
CREATE TABLE Product (
    product_id INT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    price DECIMAL(10,2) NOT NULL,
    stock_quantity INT NOT NULL,
    category_id INT NOT NULL,
    supplier_id INT NOT NULL,
    FOREIGN KEY (category_id) REFERENCES Category(category_id),
    FOREIGN KEY (supplier_id) REFERENCES Supplier(supplier_id)
);

-- Product Image Table
CREATE TABLE ProductImage (
    image_id INT PRIMARY KEY,
    product_id INT NOT NULL,
    image_url TEXT NOT NULL,
    FOREIGN KEY (product_id) REFERENCES Product(product_id)
);

-- Cart Table
CREATE TABLE Cart (
    cart_id INT PRIMARY KEY,
    customer_id INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (customer_id) REFERENCES Customer(customer_id)
);

-- CartItem Table
CREATE TABLE CartItem (
    cartitem_id INT PRIMARY KEY,
    cart_id INT NOT NULL,
    product_id INT NOT NULL,
    quantity INT NOT NULL,
    FOREIGN KEY (cart_id) REFERENCES Cart(cart_id),
    FOREIGN KEY (product_id) REFERENCES Product(product_id)
);
-- Discount Table
CREATE TABLE Discount (
    discount_id INT PRIMARY KEY,
    code VARCHAR(50) UNIQUE NOT NULL,
    description TEXT,
    discount_percent DECIMAL(5,2),
    valid_from DATE,
    valid_to DATE
);


-- Orders Table
CREATE TABLE Orders (
    order_id INT PRIMARY KEY,
    customer_id INT NOT NULL,
    order_date DATE NOT NULL,
    total_amount DECIMAL(10,2) NOT NULL,
    current_status VARCHAR(50) NOT NULL,
    discount_id INT,
    shipping_address_id INT NOT NULL,
    FOREIGN KEY (customer_id) REFERENCES Customer(customer_id),
    FOREIGN KEY (discount_id) REFERENCES Discount(discount_id),
    FOREIGN KEY (shipping_address_id) REFERENCES CustomerAddress(address_id)
);

-- Order Item Table
CREATE TABLE OrderItem (
    order_item_id INT PRIMARY KEY,
    order_id INT NOT NULL,
    product_id INT NOT NULL,
    quantity INT NOT NULL,
    price DECIMAL(10,2) NOT NULL,
    FOREIGN KEY (order_id) REFERENCES Orders(order_id),
    FOREIGN KEY (product_id) REFERENCES Product(product_id)
);

-- Order Status History Table
CREATE TABLE OrderStatusHistory (
    status_id INT PRIMARY KEY,
    order_id INT NOT NULL,
    status VARCHAR(50) NOT NULL,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (order_id) REFERENCES Orders(order_id)
);

-- Delivery Table
CREATE TABLE Delivery (
    delivery_id INT PRIMARY KEY,
    order_id INT NOT NULL,
    status VARCHAR(50) NOT NULL,
    delivery_date DATE,
    FOREIGN KEY (order_id) REFERENCES Orders(order_id)
);


-- Transactions Table
CREATE TABLE Transactions (
    transaction_id INT PRIMARY KEY,
    order_id INT NOT NULL,
    amount DECIMAL(10,2) NOT NULL,
    status VARCHAR(50) NOT NULL,
    transaction_date DATE NOT NULL,
    method VARCHAR(50),
    FOREIGN KEY (order_id) REFERENCES Orders(order_id)
);