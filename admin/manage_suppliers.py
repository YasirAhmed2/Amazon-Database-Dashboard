import streamlit as st
from sqlalchemy import text
from db.connection import get_engine

def manage_suppliers():
    st.title("🏭 Manage Suppliers")

    engine = get_engine()
    with engine.begin() as conn:
        # Add new supplier
        st.subheader("➕ Add New Supplier")
        name = st.text_input("Supplier Name")
        email = st.text_input("Email")
        phone = st.text_input("Phone")

        if st.button("Add Supplier"):
            if not name.strip() or not email.strip():
                st.warning("Name and Email are required.")
            else:
                try:
                    conn.execute(text("""
                        INSERT INTO Supplier (name, email, phone)
                        VALUES (:name, :email, :phone)
                    """), {"name": name, "email": email, "phone": phone})
                    st.success(f"Supplier '{name}' added successfully.")
                except Exception as e:
                    st.error(f"Error: {e}")

        st.divider()

        # List and delete existing suppliers
        st.subheader("📋 Existing Suppliers")
        result = conn.execute(text("SELECT supplier_id, name, email, phone FROM Supplier")).fetchall()

        for sup in result:
            col1, col2 = st.columns([4, 1])
            with col1:
                st.write(f"🆔 {sup.supplier_id} | **{sup.name}** - {sup.email} | 📞 {sup.phone or 'N/A'}")
            with col2:
                if st.button("🗑️ Delete", key=f"del_sup_{sup.supplier_id}"):
                    conn.execute(text("DELETE FROM Supplier WHERE supplier_id = :id"), {"id": sup.supplier_id})
                    st.success(f"Deleted supplier: {sup.name}")
                    st.rerun()
