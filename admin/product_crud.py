import streamlit as st
from sqlalchemy import text
from db.connection import get_engine

def load_categories(conn):
    query = text("SELECT category_id, category_name FROM Category")
    return conn.execute(query).fetchall()

def get_supplier_id(conn, supplier_name):
    # Check if supplier exists
    result = conn.execute(text("SELECT supplier_id FROM Supplier WHERE name = :name"), {"name": supplier_name}).fetchone()
    if result:
        return result.supplier_id
    # If not, create new supplier
    conn.execute(text("INSERT INTO Supplier (name, email, phone) VALUES (:name, '', '')"), {"name": supplier_name})
    return conn.execute(text("SELECT supplier_id FROM Supplier WHERE name = :name"), {"name": supplier_name}).fetchone().supplier_id

def list_products(conn):
    return conn.execute(text("""
        SELECT p.product_id, p.name, p.price, p.stock_quantity, c.category_name, s.name as supplier
        FROM Product p
        JOIN Category c ON p.category_id = c.category_id
        JOIN Supplier s ON p.supplier_id = s.supplier_id
    """)).fetchall()

def product_crud():
    st.title("🛠 Product Management")

    engine = get_engine()
    with engine.begin() as conn:
        categories = load_categories(conn)
        category_dict = {c.category_name: c.category_id for c in categories}

        st.subheader("➕ Add New Product")
        name = st.text_input("Product Name")
        description = st.text_area("Description")
        price = st.number_input("Price", min_value=0.0)
        quantity = st.number_input("Stock Quantity", min_value=0)
        category = st.selectbox("Category", options=list(category_dict.keys()))
        supplier_name = st.text_input("Supplier Name")

        if st.button("Add Product"):
            supplier_id = get_supplier_id(conn, supplier_name)
            conn.execute(text("""
                INSERT INTO Product (name, description, price, stock_quantity, category_id, supplier_id)
                VALUES (:name, :desc, :price, :qty, :cat_id, :sup_id)
            """), {
                "name": name, "desc": description, "price": price,
                "qty": quantity, "cat_id": category_dict[category],
                "sup_id": supplier_id
            })
            st.success("✅ Product added successfully!")

        st.subheader("📋 Existing Products")
        products = list_products(conn)
        for product in products:
            with st.expander(f"{product.name} (ID: {product.product_id})"):
                st.text(f"Price: {product.price}")
                st.text(f"Stock: {product.stock_quantity}")
                st.text(f"Category: {product.category_name}")
                st.text(f"Supplier: {product.supplier}")
                
                if st.button(f"❌ Delete Product ID {product.product_id}"):
                    conn.execute(text("DELETE FROM Product WHERE product_id = :id"), {"id": product.product_id})
                    st.success("🗑 Product deleted. Please refresh.")

