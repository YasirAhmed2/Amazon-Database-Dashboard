import streamlit as st
from db import get_connection

def customer_dashboard():
    st.title("Welcome to Customer Dashboard")
    st.markdown(f"Logged in as: `{st.session_state.customer_id}`")

    menu = ["My Orders", "Browse Products", "Update Profile", "Logout"]
    choice = st.selectbox("Menu", menu)

    if choice == "My Orders":
        st.subheader("Your Orders")
        conn = get_connection()
        orders = conn.execute("SELECT * FROM orders WHERE customer_id = %s", (st.session_state.customer_id,))
        for row in orders:
            st.json(dict(row))

    elif choice == "Browse Products":
        st.subheader("Product Catalog")
        conn = get_connection()
        rows = conn.execute("SELECT * FROM product LIMIT 100").fetchall()
        for row in rows:
            st.markdown(f"**{row['name']}** - {row['price']} PKR")

    elif choice == "Update Profile":
        st.warning("Update feature coming soon!")

    elif choice == "Logout":
        st.session_state.clear()
        st.experimental_rerun()
