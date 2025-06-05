import streamlit as st
from admin.login import admin_login
from admin.product_crud import product_crud
from admin.view_orders import view_orders
from admin.manage_categories import manage_categories
from admin.manage_suppliers import manage_suppliers

st.set_page_config(page_title="E-Commerce Admin Panel", layout="wide")

if "admin_logged_in" not in st.session_state or not st.session_state.admin_logged_in:
    admin_login()
else:
    st.sidebar.title("Admin Menu")
    choice = st.sidebar.radio("Choose Action", [
        "Product Management", 
        "View Orders", 
        "Manage Categories", 
        "Manage Suppliers", 
        "Logout"
    ])

    if choice == "Product Management":
        product_crud()
    elif choice == "View Orders":
        view_orders()
    elif choice == "Manage Categories":
        manage_categories()
    elif choice == "Manage Suppliers":
        manage_suppliers()
    elif choice == "Logout":
        st.session_state.clear()
        st.experimental_rerun()
