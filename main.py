import streamlit as st

# Admin imports
from admin.login import admin_login
from admin.product_crud import product_crud
from admin.view_orders import view_orders
from admin.manage_categories import manage_categories
from admin.manage_suppliers import manage_suppliers

# Customer imports
from customer.auth import login_customer, signup_customer
from customer.dashboard import customer_dashboard

# Streamlit config
st.set_page_config("Amazon Dashboard", layout="wide")

# Session defaults
if "admin_logged_in" not in st.session_state:
    st.session_state.admin_logged_in = False

if "is_customer_logged_in" not in st.session_state:
    st.session_state.is_customer_logged_in = False

def show_home():
    st.title("Amazon DB Dashboard")
    st.markdown("Welcome to the Amazon-style dashboard. Please choose a role from the sidebar.")

# Sidebar Navigation
with st.sidebar:
    if not st.session_state.admin_logged_in and not st.session_state.is_customer_logged_in:
        role = st.selectbox("Choose Role", ["Home", "Admin Login", "Customer Login", "Customer Signup"])
    elif st.session_state.admin_logged_in:
        role = "Admin Panel"
    elif st.session_state.is_customer_logged_in:
        role = "Customer Panel"

# ---------- ROUTING ----------
# Home view
if role == "Home":
    show_home()

# ---------- Admin Flow ----------
elif role == "Admin Login":
    admin_login()

elif role == "Admin Panel":
    st.sidebar.title("Admin Panel")
    admin_option = st.sidebar.radio("Choose Action", [
        "Product Management",
        "View Orders",
        "Manage Categories",
        "Manage Suppliers",
        "Logout"
    ])

    if admin_option == "Product Management":
        product_crud()
    elif admin_option == "View Orders":
        view_orders()
    elif admin_option == "Manage Categories":
        manage_categories()
    elif admin_option == "Manage Suppliers":
        manage_suppliers()
    elif admin_option == "Logout":
        st.session_state.admin_logged_in = False
        st.rerun()

# ---------- Customer Flow ----------
elif role == "Customer Login":
    login_customer()

elif role == "Customer Signup":
    signup_customer()

elif role == "Customer Panel":
    customer_dashboard()
