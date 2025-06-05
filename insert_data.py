import psycopg2
from faker import Faker
import random
from datetime import datetime, timedelta
import time
from tqdm import tqdm
import uuid

# Initialize Faker
fake = Faker()

# Database connection parameters
DB_NAME = "amazon"
DB_USER = "yasir2"
DB_PASSWORD = "uiop12345"
DB_HOST = "localhost"
DB_PORT = "32769"

def get_db_connection():
    """Establish database connection"""
    try:
        conn = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        )
        return conn
    except Exception as e:
        print(f"Error connecting to database: {e}")
        return None

def execute_batch_insert(conn, query, data, batch_size=100, desc="Inserting"):
    """Helper function to execute batch inserts with progress tracking"""
    cursor = conn.cursor()
    try:
        for i in tqdm(range(0, len(data), batch_size), desc=desc):
            batch = data[i:i + batch_size]
            cursor.executemany(query, batch)
            conn.commit()
            time.sleep(0.1)
    except Exception as e:
        print(f"Error during batch insert: {e}")
        conn.rollback()
    finally:
        cursor.close()

def insert_customers(num_records=1000):
    """Insert dummy data into Customer table"""
    conn = get_db_connection()
    if not conn:
        return
    
    data = []
    for i in range(num_records):
        data.append((
            fake.unique.random_number(digits=8),  # customer_id
            fake.name(),                         # name
            fake.unique.email(),                 # email
            fake.phone_number(),                 # phone
            fake.date_time_between(start_date='-2y', end_date='now'),  # created_at
            fake.date_time_between(start_date='-2y', end_date='now')   # updated_at
        ))
    
    query = """
    INSERT INTO Customer (customer_id, name, email, phone, created_at, updated_at)
    VALUES (%s, %s, %s, %s, %s, %s)
    """
    
    execute_batch_insert(conn, query, data, desc="Inserting Customers")
    conn.close()

def insert_admins(num_records=1000):
    """Insert dummy data into Admin table"""
    conn = get_db_connection()
    if not conn:
        return
    
    data = []
    for i in range(num_records):
        data.append((
            fake.unique.random_number(digits=8),  # admin_id
            fake.name(),                         # name
            fake.unique.email(),                 # email
            fake.unique.user_name(),             # user_name
            fake.password(length=12),            # password
            fake.date_time_between(start_date='-2y', end_date='now'),  # created_at
            fake.date_time_between(start_date='-2y', end_date='now')   # updated_at
        ))
    
    query = """
    INSERT INTO Admin (admin_id, name, email, user_name, password, created_at, updated_at)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    
    execute_batch_insert(conn, query, data, desc="Inserting Admins")
    conn.close()

def insert_suppliers(num_records=1000):
    """Insert dummy data into Supplier table"""
    conn = get_db_connection()
    if not conn:
        return
    
    data = []
    for i in range(num_records):
        data.append((
            fake.unique.random_number(digits=8),  # supplier_id
            fake.company(),                      # name
            fake.unique.company_email(),        # email
            fake.phone_number()                 # phone
        ))
    
    query = """
    INSERT INTO Supplier (supplier_id, name, email, phone)
    VALUES (%s, %s, %s, %s)
    """
    
    execute_batch_insert(conn, query, data, desc="Inserting Suppliers")
    conn.close()

def insert_categories(num_records=1000):
    """Insert dummy data into Category table"""
    conn = get_db_connection()
    if not conn:
        return
    
    # Create some realistic product categories
    categories = [
        "Electronics", "Clothing", "Home & Garden", "Books", "Toys",
        "Sports", "Beauty", "Health", "Automotive", "Groceries"
    ]
    
    data = []
    for i in range(num_records):
        category_name = f"{random.choice(categories)} - {fake.word()}"
        data.append((
            fake.unique.random_number(digits=8),  # category_id
            category_name                       # category_name
        ))
    
    query = """
    INSERT INTO Category (category_id, category_name)
    VALUES (%s, %s)
    """
    
    execute_batch_insert(conn, query, data, desc="Inserting Categories")
    conn.close()

def insert_products(num_records=1000):
    """Insert dummy data into Product table with FK validation"""
    conn = get_db_connection()
    if not conn:
        return
    
    # Get foreign key references with validation
    cursor = conn.cursor()
    cursor.execute("SELECT category_id FROM Category")
    category_ids = [row[0] for row in cursor.fetchall()]
    
    cursor.execute("SELECT supplier_id FROM Supplier")
    supplier_ids = [row[0] for row in cursor.fetchall()]
    cursor.close()
    
    if not category_ids:
        print("Error: No categories found. Please insert categories first.")
        conn.close()
        return
    
    if not supplier_ids:
        print("Error: No suppliers found. Please insert suppliers first.")
        conn.close()
        return
    
    data = []
    for i in range(num_records):
        data.append((
            fake.unique.random_number(digits=8),
            fake.catch_phrase()[:100],
            fake.text(max_nb_chars=200),
            round(random.uniform(1, 1000), 2),
            random.randint(0, 1000),
            random.choice(category_ids),
            random.choice(supplier_ids)
        ))
    
    query = """
    INSERT INTO Product (product_id, name, description, price, stock_quantity, category_id, supplier_id)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    
    execute_batch_insert(conn, query, data, desc="Inserting Products")
    conn.close()

def insert_discounts(num_records=1000):
    """Insert dummy data into Discount table"""
    conn = get_db_connection()
    if not conn:
        return
    
    data = []
    for i in range(num_records):
        valid_from = fake.date_between(start_date='-1y', end_date='today')
        valid_to = fake.date_between(start_date=valid_from, end_date='+1y')
        data.append((
            fake.unique.random_number(digits=8),  # discount_id
            fake.unique.bothify(text='DISCOUNT-#####'),  # code
            fake.sentence(),                      # description
            round(random.uniform(1, 50), 2),     # discount_percent
            valid_from,                          # valid_from
            valid_to                            # valid_to
        ))
    
    query = """
    INSERT INTO Discount (discount_id, code, description, discount_percent, valid_from, valid_to)
    VALUES (%s, %s, %s, %s, %s, %s)
    """
    
    execute_batch_insert(conn, query, data, desc="Inserting Discounts")
    conn.close()

def insert_customer_addresses(num_records=1000):
    """Insert dummy data into CustomerAddress table"""
    conn = get_db_connection()
    if not conn:
        return
    
    # Get customer IDs
    cursor = conn.cursor()
    cursor.execute("SELECT customer_id FROM Customer")
    customer_ids = [row[0] for row in cursor.fetchall()]
    cursor.close()
    
    data = []
    for i in range(num_records):
        data.append((
            fake.unique.random_number(digits=8),  # address_id
            random.choice(customer_ids),         # customer_id
            fake.address().replace('\n', ', '),  # address
            fake.city(),                         # city
            fake.state(),                        # state
            fake.postcode(),                     # postal_code
            fake.country()                       # country
        ))
    
    query = """
    INSERT INTO CustomerAddress (address_id, customer_id, address, city, state, postal_code, country)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    
    execute_batch_insert(conn, query, data, desc="Inserting Customer Addresses")
    conn.close()

def insert_admin_logins(num_records=1000):
    """Insert dummy data into AdminLogin table"""
    conn = get_db_connection()
    if not conn:
        return
    
    # Get admin IDs
    cursor = conn.cursor()
    cursor.execute("SELECT admin_id FROM Admin")
    admin_ids = [row[0] for row in cursor.fetchall()]
    cursor.close()
    
    data = []
    for i in range(num_records):
        data.append((
            fake.unique.random_number(digits=8),  # login_id
            random.choice(admin_ids),            # admin_id
            fake.date_time_between(start_date='-2y', end_date='now')  # login_time
        ))
    
    query = """
    INSERT INTO AdminLogin (login_id, admin_id, login_time)
    VALUES (%s, %s, %s)
    """
    
    execute_batch_insert(conn, query, data, desc="Inserting Admin Logins")
    conn.close()

def insert_customer_logins(num_records=1000):
    """Insert dummy data into CustomerLogin table"""
    conn = get_db_connection()
    if not conn:
        return
    
    # Get customer IDs
    cursor = conn.cursor()
    cursor.execute("SELECT customer_id FROM Customer")
    customer_ids = [row[0] for row in cursor.fetchall()]
    cursor.close()
    
    data = []
    for i in range(num_records):
        data.append((
            fake.unique.random_number(digits=8),  # login_id
            random.choice(customer_ids),         # customer_id
            fake.date_time_between(start_date='-2y', end_date='now')  # login_time
        ))
    
    query = """
    INSERT INTO CustomerLogin (login_id, customer_id, login_time)
    VALUES (%s, %s, %s)
    """
    
    execute_batch_insert(conn, query, data, desc="Inserting Customer Logins")
    conn.close()

def insert_product_images(num_records=1000):
    """Insert dummy data into ProductImage table"""
    conn = get_db_connection()
    if not conn:
        return
    
    # Get product IDs
    cursor = conn.cursor()
    cursor.execute("SELECT product_id FROM Product")
    product_ids = [row[0] for row in cursor.fetchall()]
    cursor.close()
    
    data = []
    for i in range(num_records):
        data.append((
            fake.unique.random_number(digits=8),  # image_id
            random.choice(product_ids),          # product_id
            f'https://example.com/images/{fake.uuid4()}.jpg'  # image_url
        ))
    
    query = """
    INSERT INTO ProductImage (image_id, product_id, image_url)
    VALUES (%s, %s, %s)
    """
    
    execute_batch_insert(conn, query, data, desc="Inserting Product Images")
    conn.close()

def insert_carts(num_records=1000):
    """Insert dummy data into Cart table"""
    conn = get_db_connection()
    if not conn:
        return
    
    # Get customer IDs
    cursor = conn.cursor()
    cursor.execute("SELECT customer_id FROM Customer")
    customer_ids = [row[0] for row in cursor.fetchall()]
    cursor.close()
    
    data = []
    for i in range(num_records):
        data.append((
            fake.unique.random_number(digits=8),  # cart_id
            random.choice(customer_ids),         # customer_id
            fake.date_time_between(start_date='-2y', end_date='now')  # created_at
        ))
    
    query = """
    INSERT INTO Cart (cart_id, customer_id, created_at)
    VALUES (%s, %s, %s)
    """
    
    execute_batch_insert(conn, query, data, desc="Inserting Carts")
    conn.close()

def insert_cart_items(num_records=1000):
    """Insert dummy data into CartItem table"""
    conn = get_db_connection()
    if not conn:
        return
    
    # Get cart and product IDs
    cursor = conn.cursor()
    cursor.execute("SELECT cart_id FROM Cart")
    cart_ids = [row[0] for row in cursor.fetchall()]
    
    cursor.execute("SELECT product_id FROM Product")
    product_ids = [row[0] for row in cursor.fetchall()]
    cursor.close()
    
    data = []
    for i in range(num_records):
        data.append((
            fake.unique.random_number(digits=8),  # cartitem_id
            random.choice(cart_ids),             # cart_id
            random.choice(product_ids),          # product_id
            random.randint(1, 10)               # quantity
        ))
    
    query = """
    INSERT INTO CartItem (cartitem_id, cart_id, product_id, quantity)
    VALUES (%s, %s, %s, %s)
    """
    
    execute_batch_insert(conn, query, data, desc="Inserting Cart Items")
    conn.close()

def insert_orders(num_records=1000):
    """Insert dummy data into Orders table"""
    conn = get_db_connection()
    if not conn:
        return
    
    # Get foreign key references
    cursor = conn.cursor()
    cursor.execute("SELECT customer_id FROM Customer")
    customer_ids = [row[0] for row in cursor.fetchall()]
    
    cursor.execute("SELECT discount_id FROM Discount")
    discount_ids = [row[0] for row in cursor.fetchall()]
    
    cursor.execute("SELECT address_id FROM CustomerAddress")
    address_ids = [row[0] for row in cursor.fetchall()]
    cursor.close()
    
    statuses = ['pending', 'processing', 'completed', 'cancelled']
    
    data = []
    for i in range(num_records):
        data.append((
            fake.unique.random_number(digits=8),  # order_id
            random.choice(customer_ids),         # customer_id
            fake.date_between(start_date='-2y', end_date='today'),  # order_date
            round(random.uniform(10, 1000), 2),  # total_amount
            random.choice(statuses),             # current_status
            random.choice(discount_ids + [None]),  # discount_id (some may be NULL)
            random.choice(address_ids)          # shipping_address_id
        ))
    
    query = """
    INSERT INTO Orders (order_id, customer_id, order_date, total_amount, current_status, discount_id, shipping_address_id)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    
    execute_batch_insert(conn, query, data, desc="Inserting Orders")
    conn.close()

def insert_order_items(num_records=1000):
    """Insert dummy data into OrderItem table"""
    conn = get_db_connection()
    if not conn:
        return
    
    # Get foreign key references
    cursor = conn.cursor()
    cursor.execute("SELECT order_id FROM Orders")
    order_ids = [row[0] for row in cursor.fetchall()]
    
    cursor.execute("SELECT product_id FROM Product")
    product_ids = [row[0] for row in cursor.fetchall()]
    cursor.close()
    
    data = []
    for i in range(num_records):
        data.append((
            fake.unique.random_number(digits=8),  # order_item_id
            random.choice(order_ids),            # order_id
            random.choice(product_ids),         # product_id
            random.randint(1, 10),              # quantity
            round(random.uniform(5, 500), 2)    # price
        ))
    
    query = """
    INSERT INTO OrderItem (order_item_id, order_id, product_id, quantity, price)
    VALUES (%s, %s, %s, %s, %s)
    """
    
    execute_batch_insert(conn, query, data, desc="Inserting Order Items")
    conn.close()

def insert_order_status_history(num_records=1000):
    """Insert dummy data into OrderStatusHistory table"""
    conn = get_db_connection()
    if not conn:
        return
    
    # Get order IDs
    cursor = conn.cursor()
    cursor.execute("SELECT order_id FROM Orders")
    order_ids = [row[0] for row in cursor.fetchall()]
    cursor.close()
    
    statuses = ['pending', 'processing', 'shipped', 'delivered', 'cancelled']
    
    data = []
    for i in range(num_records):
        data.append((
            fake.unique.random_number(digits=8),  # status_id
            random.choice(order_ids),            # order_id
            random.choice(statuses),             # status
            fake.date_time_between(start_date='-2y', end_date='now')  # updated_at
        ))
    
    query = """
    INSERT INTO OrderStatusHistory (status_id, order_id, status, updated_at)
    VALUES (%s, %s, %s, %s)
    """
    
    execute_batch_insert(conn, query, data, desc="Inserting Order Status History")
    conn.close()

def insert_deliveries(num_records=1000):
    """Insert dummy data into Delivery table"""
    conn = get_db_connection()
    if not conn:
        return
    
    # Get order IDs
    cursor = conn.cursor()
    cursor.execute("SELECT order_id FROM Orders")
    order_ids = [row[0] for row in cursor.fetchall()]
    cursor.close()
    
    statuses = ['pending', 'shipped', 'in_transit', 'delivered', 'failed']
    
    data = []
    for i in range(num_records):
        status = random.choice(statuses)
        delivery_date = fake.date_between(start_date='-2y', end_date='today') if status in ['delivered', 'in_transit'] else None
        data.append((
            fake.unique.random_number(digits=8),  # delivery_id
            random.choice(order_ids),            # order_id
            status,                              # status
            delivery_date                       # delivery_date
        ))
    
    query = """
    INSERT INTO Delivery (delivery_id, order_id, status, delivery_date)
    VALUES (%s, %s, %s, %s)
    """
    
    execute_batch_insert(conn, query, data, desc="Inserting Deliveries")
    conn.close()

def insert_transactions(num_records=1000):
    """Insert dummy data into Transactions table"""
    conn = get_db_connection()
    if not conn:
        return
    
    # Get order IDs
    cursor = conn.cursor()
    cursor.execute("SELECT order_id FROM Orders")
    order_ids = [row[0] for row in cursor.fetchall()]
    cursor.close()
    
    methods = ['credit_card', 'paypal', 'bank_transfer', 'crypto']
    statuses = ['completed', 'pending', 'failed', 'refunded']
    
    data = []
    for i in range(num_records):
        data.append((
            fake.unique.random_number(digits=8),  # transaction_id
            random.choice(order_ids),            # order_id
            round(random.uniform(10, 1000), 2),  # amount
            random.choice(statuses),             # status
            fake.date_between(start_date='-2y', end_date='today'),  # transaction_date
            random.choice(methods)              # method
        ))
    
    query = """
    INSERT INTO Transactions (transaction_id, order_id, amount, status, transaction_date, method)
    VALUES (%s, %s, %s, %s, %s, %s)
    """
    
    execute_batch_insert(conn, query, data, desc="Inserting Transactions")
    conn.close()

def main():
    """Main function with proper error handling"""
    print("Starting data generation (100000 records per table)...")
    
    try:
        # Independent tables (must succeed first)
        print("\n=== Inserting Independent Tables ===")
        insert_customers()
        insert_admins()
        insert_suppliers()
        insert_categories()
        insert_discounts()
        
        # Products depends on categories and suppliers
        print("\n=== Inserting Products ===")
        insert_products()
        
        # Tables that depend on customers
        print("\n=== Inserting Customer-Related Tables ===")
        insert_customer_addresses()
        insert_customer_logins()
        insert_carts()
        
        # Tables that depend on products
        print("\n=== Inserting Product-Related Tables ===")
        insert_product_images()
        insert_cart_items()
        
        # Orders depend on customers, discounts, and addresses
        print("\n=== Inserting Orders ===")
        insert_orders()
        
        # These depend on orders
        print("\n=== Inserting Order-Related Tables ===")
        insert_order_items()
        insert_order_status_history()
        insert_deliveries()
        insert_transactions()
        
        # Admin logins depend on admins
        print("\n=== Inserting Admin Logins ===")
        insert_admin_logins()
        
        print("\nData generation completed successfully!")
        
    except Exception as e:
        print(f"\nError during data generation: {e}")
        print("Please check the error message and fix the issue.")

if __name__ == "__main__":
    main()