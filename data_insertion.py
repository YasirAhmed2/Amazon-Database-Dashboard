import csv
import random
import psycopg2
from faker import Faker
from datetime import datetime, timedelta
import uuid
import numpy as np
from tqdm import tqdm
from psycopg2 import sql
from psycopg2.extras import execute_batch

# Configuration
RECORDS_PER_TABLE = 100000  # 100,000 records per table
CHUNK_SIZE = 10000  # Batch insert size

# Database connection parameters - UPDATE THESE FOR YOUR DATABASE
DB_CONFIG = {
    'host': 'localhost',
    'database': 'amazon',
    'user': 'yasir2',
    'password': 'uiop12345',
    'port': '32768'
}

fake = Faker()

# Track generated data to maintain referential integrity
generated_data = {
    'admin': [],
    'customer': [],
    'category': [],
    'supplier': [],
    'product': [],
    'cart': [],
    'discount': [],
    'customeraddress': [],
    'orders': [],
    'orderitem': [],
    'delivery': [],
    'transactions': [],
    'productimage': [],
    'adminlogin': [],
    'customerlogin': [],
    'orderstatushistory': []
}

def get_db_connection():
    """Establish database connection"""
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        return conn
    except Exception as e:
        print(f"Error connecting to database: {e}")
        raise

def execute_insert(conn, table_name, data):
    """Execute batch insert for a table"""
    if not data:
        return
    
    columns = data[0].keys()
    query = sql.SQL("INSERT INTO {} ({}) VALUES ({})").format(
        sql.Identifier(table_name),
        sql.SQL(', ').join(map(sql.Identifier, columns)),
        sql.SQL(', ').join(sql.Placeholder() * len(columns))
    )
    try:
        with conn.cursor() as cursor:
            values = [tuple(row[col] for col in columns) for row in data]
            execute_batch(cursor, query, values, page_size=CHUNK_SIZE)
        conn.commit()
    except Exception as e:
        conn.rollback()
        print(f"Error inserting into {table_name}: {e}")
        raise

def generate_admin_data(conn):
    print("\nGenerating admin data...")
    data = []
    for i in tqdm(range(1, RECORDS_PER_TABLE + 1), desc="Admins"):
        admin = {
            'admin_id': i,
            'name': fake.unique.name(),
            'email': f"admin{i}@example.com",  # Ensures unique email
            'user_name': f"admin_{i}",  # Ensures unique username
            'password': str(uuid.uuid4()),  # Random password hash
            'created_at': fake.date_time_this_decade(),
            'updated_at': fake.date_time_this_decade()
        }
        data.append(admin)
        if len(data) >= CHUNK_SIZE:
            execute_insert(conn, 'admin', data)
            generated_data['admin'].extend(data)
            data = []
    
    if data:
        execute_insert(conn, 'admin', data)
        generated_data['admin'].extend(data)

def generate_customer_data(conn):
    print("\nGenerating customer data...")
    data = []
    for i in tqdm(range(1, RECORDS_PER_TABLE + 1), desc="Customers"):
        customer = {
            'customer_id': i,
            'name': fake.unique.name(),
            'email': f"customer{i}@example.com",  # Ensures unique email
            'phone': fake.unique.phone_number()[:20],
            'created_at': fake.date_time_this_decade(),
            'updated_at': fake.date_time_this_decade(),
            'password': str(uuid.uuid4())  # Random password hash
        }
        data.append(customer)
        if len(data) >= CHUNK_SIZE:
            execute_insert(conn, 'customer', data)
            generated_data['customer'].extend(data)
            data = []
    
    if data:
        execute_insert(conn, 'customer', data)
        generated_data['customer'].extend(data)

def generate_category_data(conn):
    print("\nGenerating category data...")
    data = []
    category_words = [
        "Electronics", "Clothing", "Home", "Garden", "Sports", "Books", 
        "Toys", "Health", "Beauty", "Automotive", "Tools", "Jewelry", 
        "Food", "Pet", "Baby", "Office", "Furniture", "Music", "Movies"
    ]
    subcategory_words = [
        "Accessories", "Supplies", "Equipment", "Gear", "Essentials",
        "Collections", "Systems", "Solutions", "Products", "Items",
        "Goods", "Merchandise", "Wear", "Kits", "Sets", "Packs"
    ]
    
    for i in tqdm(range(1, RECORDS_PER_TABLE + 1), desc="Categories"):
        main_word = random.choice(category_words)
        sub_word = random.choice(subcategory_words)
        category_name = f"{main_word} {sub_word} {i}"
        
        category = {
            'category_id': i,
            'category_name': category_name
        }
        data.append(category)
        if len(data) >= CHUNK_SIZE:
            execute_insert(conn, 'category', data)
            generated_data['category'].extend(data)
            data = []
    
    if data:
        execute_insert(conn, 'category', data)
        generated_data['category'].extend(data)

def generate_supplier_data(conn):
    print("\nGenerating supplier data...")
    data = []
    for i in tqdm(range(1, RECORDS_PER_TABLE + 1), desc="Suppliers"):
        supplier = {
            'supplier_id': i,
            'name': f"{fake.unique.company()} {i}",
            'email': f"supplier{i}@example.com",
            'phone': fake.unique.phone_number()[:20]
        }
        data.append(supplier)
        if len(data) >= CHUNK_SIZE:
            execute_insert(conn, 'supplier', data)
            generated_data['supplier'].extend(data)
            data = []
    
    if data:
        execute_insert(conn, 'supplier', data)
        generated_data['supplier'].extend(data)

def generate_product_data(conn):
    print("\nGenerating product data...")
    data = []
    for i in tqdm(range(1, RECORDS_PER_TABLE + 1), desc="Products"):
        product = {
            'product_id': i,
            'name': f"{fake.unique.catch_phrase()} {i}",
            'description': fake.text(max_nb_chars=200),
            'price': round(random.uniform(1, 1000), 2),
            'stock_quantity': random.randint(0, 1000),
            'category_id': random.choice(generated_data['category'])['category_id'],
            'supplier_id': random.choice(generated_data['supplier'])['supplier_id']
        }
        data.append(product)
        if len(data) >= CHUNK_SIZE:
            execute_insert(conn, 'product', data)
            generated_data['product'].extend(data)
            data = []
    
    if data:
        execute_insert(conn, 'product', data)
        generated_data['product'].extend(data)

def generate_cart_data(conn):
    print("\nGenerating cart data...")
    data = []
    for i in tqdm(range(1, RECORDS_PER_TABLE + 1), desc="Carts"):
        cart = {
            'cart_id': i,
            'customer_id': random.choice(generated_data['customer'])['customer_id'],
            'created_at': fake.date_time_this_year()
        }
        data.append(cart)
        if len(data) >= CHUNK_SIZE:
            execute_insert(conn, 'cart', data)
            generated_data['cart'].extend(data)
            data = []
    
    if data:
        execute_insert(conn, 'cart', data)
        generated_data['cart'].extend(data)

def generate_cartitem_data(conn):
    print("\nGenerating cartitem data...")
    data = []
    for i in tqdm(range(1, RECORDS_PER_TABLE + 1), desc="Cart Items"):
        cartitem = {
            'cartitem_id': i,
            'cart_id': random.choice(generated_data['cart'])['cart_id'],
            'product_id': random.choice(generated_data['product'])['product_id'],
            'quantity': random.randint(1, 10)
        }
        data.append(cartitem)
        if len(data) >= CHUNK_SIZE:
            execute_insert(conn, 'cartitem', data)
            generated_data['cartitem'].extend(data)
            data = []
    
    if data:
        execute_insert(conn, 'cartitem', data)
        generated_data['cartitem'].extend(data)

def generate_customeraddress_data(conn):
    print("\nGenerating customeraddress data...")
    data = []
    for i in tqdm(range(1, RECORDS_PER_TABLE + 1), desc="Addresses"):
        customer = random.choice(generated_data['customer'])
        address = {
            'address_id': i,
            'customer_id': customer['customer_id'],
            'address': fake.unique.street_address(),
            'city': fake.city(),
            'state': fake.state(),
            'postal_code': fake.postcode(),
            'country': fake.country()
        }
        data.append(address)
        if len(data) >= CHUNK_SIZE:
            execute_insert(conn, 'customeraddress', data)
            generated_data['customeraddress'].extend(data)
            data = []
    
    if data:
        execute_insert(conn, 'customeraddress', data)
        generated_data['customeraddress'].extend(data)

def generate_discount_data(conn):
    print("\nGenerating discount data...")
    data = []
    for i in tqdm(range(1, RECORDS_PER_TABLE + 1), desc="Discounts"):
        discount = {
            'discount_id': i,
            'code': f"DIS{i:07d}",  # 7-digit unique code
            'description': fake.sentence(),
            'discount_percent': round(random.uniform(5, 50), 2),
            'valid_from': fake.date_this_year(),
            'valid_to': fake.date_between(start_date='+30d', end_date='+1y')
        }
        data.append(discount)
        if len(data) >= CHUNK_SIZE:
            execute_insert(conn, 'discount', data)
            generated_data['discount'].extend(data)
            data = []
    
    if data:
        execute_insert(conn, 'discount', data)
        generated_data['discount'].extend(data)

def generate_orders_data(conn):
    print("\nGenerating orders data...")
    data = []
    for i in tqdm(range(1, RECORDS_PER_TABLE + 1), desc="Orders"):
        customer = random.choice(generated_data['customer'])
        addresses = [addr for addr in generated_data['customeraddress'] 
                   if addr['customer_id'] == customer['customer_id']]
        
        order = {
            'order_id': i,
            'customer_id': customer['customer_id'],
            'order_date': fake.date_this_year(),
            'total_amount': round(random.uniform(10, 1000), 2),
            'current_status': random.choice(['Pending', 'Processing', 'Shipped', 'Delivered', 'Cancelled']),
            'discount_id': random.choice(generated_data['discount'])['discount_id'] if random.random() > 0.7 else None,
            'shipping_address_id': random.choice(addresses)['address_id'] if addresses else None,
            'status': random.choice(['Pending', 'Processing', 'Shipped', 'Delivered', 'Cancelled'])
        }
        data.append(order)
        if len(data) >= CHUNK_SIZE:
            execute_insert(conn, 'orders', data)
            generated_data['orders'].extend(data)
            data = []
    
    if data:
        execute_insert(conn, 'orders', data)
        generated_data['orders'].extend(data)

def generate_orderitem_data(conn):
    print("\nGenerating orderitem data...")
    data = []
    for i in tqdm(range(1, RECORDS_PER_TABLE + 1), desc="Order Items"):
        order = random.choice(generated_data['orders'])
        product = random.choice(generated_data['product'])
        orderitem = {
            'order_item_id': i,
            'order_id': order['order_id'],
            'product_id': product['product_id'],
            'quantity': random.randint(1, 5),
            'price': round(product['price'] * (1 - random.uniform(0, 0.2)), 2)  # Slight discount
        }
        data.append(orderitem)
        if len(data) >= CHUNK_SIZE:
            execute_insert(conn, 'orderitem', data)
            generated_data['orderitem'].extend(data)
            data = []
    
    if data:
        execute_insert(conn, 'orderitem', data)
        generated_data['orderitem'].extend(data)

def generate_delivery_data(conn):
    print("\nGenerating delivery data...")
    data = []
    for i in tqdm(range(1, RECORDS_PER_TABLE + 1), desc="Deliveries"):
        order = random.choice(generated_data['orders'])
        delivery = {
            'delivery_id': i,
            'order_id': order['order_id'],
            'status': random.choice(['Preparing', 'Shipped', 'In Transit', 'Delivered', 'Failed']),
            'delivery_date': fake.date_between(start_date=order['order_date'], end_date='+30d') 
                          if order['status'] in ['Shipped', 'Delivered'] else None
        }
        data.append(delivery)
        if len(data) >= CHUNK_SIZE:
            execute_insert(conn, 'delivery', data)
            generated_data['delivery'].extend(data)
            data = []
    
    if data:
        execute_insert(conn, 'delivery', data)
        generated_data['delivery'].extend(data)

def generate_transactions_data(conn):
    print("\nGenerating transactions data...")
    data = []
    for i in tqdm(range(1, RECORDS_PER_TABLE + 1), desc="Transactions"):
        order = random.choice(generated_data['orders'])
        transaction = {
            'transaction_id': i,
            'order_id': order['order_id'],
            'amount': order['total_amount'],
            'status': 'Completed' if order['status'] != 'Cancelled' else 'Refunded',
            'transaction_date': order['order_date'],
            'method': random.choice(['Credit Card', 'Debit Card', 'PayPal', 'Bank Transfer'])
        }
        data.append(transaction)
        if len(data) >= CHUNK_SIZE:
            execute_insert(conn, 'transactions', data)
            generated_data['transactions'].extend(data)
            data = []
    
    if data:
        execute_insert(conn, 'transactions', data)
        generated_data['transactions'].extend(data)

def generate_productimage_data(conn):
    print("\nGenerating productimage data...")
    data = []
    for i in tqdm(range(1, RECORDS_PER_TABLE + 1), desc="Product Images"):
        product = random.choice(generated_data['product'])
        productimage = {
            'image_id': i,
            'product_id': product['product_id'],
            'image_url': f"https://example.com/images/{product['product_id']}_{i}.jpg"
        }
        data.append(productimage)
        if len(data) >= CHUNK_SIZE:
            execute_insert(conn, 'productimage', data)
            generated_data['productimage'].extend(data)
            data = []
    
    if data:
        execute_insert(conn, 'productimage', data)
        generated_data['productimage'].extend(data)

def generate_adminlogin_data(conn):
    print("\nGenerating adminlogin data...")
    data = []
    for i in tqdm(range(1, RECORDS_PER_TABLE + 1), desc="Admin Logins"):
        adminlogin = {
            'login_id': i,
            'admin_id': random.choice(generated_data['admin'])['admin_id'],
            'login_time': fake.date_time_this_year()
        }
        data.append(adminlogin)
        if len(data) >= CHUNK_SIZE:
            execute_insert(conn, 'adminlogin', data)
            generated_data['adminlogin'].extend(data)
            data = []
    
    if data:
        execute_insert(conn, 'adminlogin', data)
        generated_data['adminlogin'].extend(data)

def generate_customerlogin_data(conn):
    print("\nGenerating customerlogin data...")
    data = []
    for i in tqdm(range(1, RECORDS_PER_TABLE + 1), desc="Customer Logins"):
        customerlogin = {
            'login_id': i,
            'customer_id': random.choice(generated_data['customer'])['customer_id'],
            'login_time': fake.date_time_this_year()
        }
        data.append(customerlogin)
        if len(data) >= CHUNK_SIZE:
            execute_insert(conn, 'customerlogin', data)
            generated_data['customerlogin'].extend(data)
            data = []
    
    if data:
        execute_insert(conn, 'customerlogin', data)
        generated_data['customerlogin'].extend(data)

def generate_orderstatushistory_data(conn):
    print("\nGenerating orderstatushistory data...")
    data = []
    status_id = 1
    for _ in tqdm(range(RECORDS_PER_TABLE), desc="Status History"):
        order = random.choice(generated_data['orders'])
        for _ in range(random.randint(1, 3)):  # 1-3 status updates per order
            status_history = {
                'status_id': status_id,
                'order_id': order['order_id'],
                'status': random.choice(['Pending', 'Processing', 'Shipped', 'Delivered', 'Cancelled']),
                'updated_at': fake.date_time_between(start_date=order['order_date'], end_date='now')
            }
            data.append(status_history)
            status_id += 1
            
            if len(data) >= CHUNK_SIZE:
                execute_insert(conn, 'orderstatushistory', data)
                generated_data['orderstatushistory'].extend(data)
                data = []
            
            if status_id > RECORDS_PER_TABLE:
                break
        
        if status_id > RECORDS_PER_TABLE:
            break
    
    if data:
        execute_insert(conn, 'orderstatushistory', data)
        generated_data['orderstatushistory'].extend(data)

def main():
    try:
        conn = get_db_connection()
        
        # Generate data in dependency order
        generate_admin_data(conn)
        generate_customer_data(conn)
        generate_category_data(conn)
        generate_supplier_data(conn)
        generate_product_data(conn)
        generate_cart_data(conn)
        generate_cartitem_data(conn)
        generate_customeraddress_data(conn)
        generate_discount_data(conn)
        generate_orders_data(conn)
        generate_orderitem_data(conn)
        generate_delivery_data(conn)
        generate_transactions_data(conn)
        generate_productimage_data(conn)
        generate_adminlogin_data(conn)
        generate_customerlogin_data(conn)
        generate_orderstatushistory_data(conn)
        
        print("\nData generation and insertion completed successfully!")
    except Exception as e:
        print(f"\nError occurred: {e}")
    finally:
        if 'conn' in locals():
            conn.close()

if __name__ == "__main__":
    main()