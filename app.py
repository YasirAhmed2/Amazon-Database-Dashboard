# app.py
import streamlit as st
import pandas as pd
from db import fetch_all, insert_record, update_record, delete_record

st.set_page_config(layout="wide")


st.title("Amazon Database Dashbaord")

table = st.selectbox("📋 Select a table", [
    "Customer", "CustomerAddress", "Admin", "AdminLogin","CustomerLogin","Supplier",
    "Category", "Product", "ProductImage", "Cart","CartItem","Discount","Orders","OrderItem",
    "OrderStatusHistory", "Delivery","Transactions"
])

# --- View Records ---
st.subheader(f"🔎 View Records from {table}")
records, columns = fetch_all(table)
df = pd.DataFrame(records, columns=columns)
st.dataframe(df, use_container_width=True)

# --- Add Record ---
with st.expander("➕ Add Record"):
    st.write("Enter data for each field below:")
    new_data = {}
    for col in columns:
        val = st.text_input(f"{col}", key=f"add_{col}")
        if val: new_data[col] = val
    if st.button("Add"):
        insert_record(table, list(new_data.keys()), list(new_data.values()))
        st.success("✅ Record added successfully")

# --- Update Record ---
with st.expander("✏️ Update Record"):
    condition_col = st.selectbox("Select ID column to update", columns)
    condition_val = st.text_input("Enter ID value to update")
    update_data = {}
    for col in columns:
        val = st.text_input(f"New value for {col}", key=f"update_{col}")
        if val: update_data[col] = val
    if st.button("Update"):
        update_record(table, update_data, (condition_col, condition_val))
        st.success("✅ Record updated successfully")

# --- Delete Record ---
with st.expander("🗑️ Delete Record"):
    del_col = st.selectbox("Select ID column to delete", columns, key="del_col")
    del_val = st.text_input("Enter ID value to delete", key="del_val")
    if st.button("Delete"):
        delete_record(table, (del_col, del_val))
        st.warning("⚠️ Record deleted")
