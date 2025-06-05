# admin/login.py

import streamlit as st
from sqlalchemy import text
from db.connection import create_engine

def admin_login():
    st.title("🔐 Admin Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        engine = get_engine()
        with engine.connect() as conn:
            query = text("""
                SELECT admin_id, name FROM Admin 
                WHERE user_name = :username AND password = :password
            """)
            result = conn.execute(query, {"username": username, "password": password}).fetchone()
            
            if result:
                st.success(f"Welcome, {result.name} 👋")
                # Save login event
                login_query = text("INSERT INTO AdminLogin (admin_id) VALUES (:admin_id)")
                conn.execute(login_query, {"admin_id": result.admin_id})
                st.session_state["admin_logged_in"] = True
                st.session_state["admin_id"] = result.admin_id
            else:
                st.error("Invalid credentials. Please try again.")
