# main.py

import streamlit as st
from admin.login import admin_login
from admin.product_crud import product_crud
from admin.view_orders import view_orders

st.set_page_config(page_title="E-Commerce Admin Panel", layout="wide")

if "admin_logged_in" not in st.session_state:
    admin_login()
else:
    st.sidebar.title("Admin Menu")
    choice = st.sidebar.radio("Choose Action", ["Product Management", "Logout"])

    if choice == "Product Management":
        product_crud()
    if choice == "View Orders":
        view_orders()
    elif choice == "Logout":
        st.session_state.clear()
