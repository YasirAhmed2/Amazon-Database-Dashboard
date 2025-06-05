import streamlit as st
from sqlalchemy import text
from db.connection import get_engine

def manage_categories():
    st.title("📂 Manage Categories")

    engine = get_engine()
    with engine.begin() as conn:
        # Add a new category
        st.subheader("➕ Add New Category")
        new_category = st.text_input("Category Name")

        if st.button("Add Category"):
            if new_category.strip() == "":
                st.warning("Please enter a valid category name.")
            else:
                try:
                    conn.execute(text("INSERT INTO Category (category_name) VALUES (:name)"), {"name": new_category})
                    st.success(f"Category '{new_category}' added successfully.")
                except Exception as e:
                    st.error(f"Error: {e}")

        st.divider()

        # List and delete existing categories
        st.subheader("📋 Existing Categories")
        result = conn.execute(text("SELECT category_id, category_name FROM Category")).fetchall()

        for cat in result:
            col1, col2 = st.columns([4, 1])
            with col1:
                st.write(f"🆔 {cat.category_id} | **{cat.category_name}**")
            with col2:
                if st.button("🗑️ Delete", key=f"del_cat_{cat.category_id}"):
                    conn.execute(text("DELETE FROM Category WHERE category_id = :id"), {"id": cat.category_id})
                    st.success(f"Deleted category: {cat.category_name}")
                    st.rerun()
