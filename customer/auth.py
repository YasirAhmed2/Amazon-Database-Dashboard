import streamlit as st
import bcrypt
from db import get_connection

def hash_password(password):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())

def check_password(password, hashed):
    return bcrypt.checkpw(password.encode(), hashed.encode())

def login_customer():
    st.title("Customer Login")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute("SELECT customer_id, password FROM customer WHERE email = %s", (email,))
            result = cur.fetchone()
            cur.close()
            conn.close()

            if result and check_password(password, result[1]):
                st.success("Login successful!")
                st.session_state.customer_id = result[0]
                st.session_state.is_customer_logged_in = True
                st.rerun()
            else:
                st.error("Invalid credentials")

        except Exception as e:
            st.error(f"Login failed: {e}")

def signup_customer():
    st.title("Customer Signup")
    name = st.text_input("Name")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Sign Up"):
        hashed_pwd = hash_password(password)

        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute(
                "INSERT INTO customer (name, email, password) VALUES (%s, %s, %s)",
                (name, email, hashed_pwd.decode())
            )
            conn.commit()
            cur.close()
            conn.close()
            st.success("Signup successful. Please log in.")
        except Exception as e:
            st.error(f"Signup failed: {str(e)}")
