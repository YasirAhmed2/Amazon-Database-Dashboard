import streamlit as st
from sqlalchemy import text
from db.connection import get_engine
from datetime import date

def view_orders():
    st.title("📦 Manage Orders")

    engine = get_engine()
    with engine.begin() as conn:

        # --- Filters and Search ---
        st.subheader("🔎 Search and Filter Orders")

        search_term = st.text_input("Search by Order ID or Customer Name")

        col1, col2 = st.columns(2)
        start_date = col1.date_input("Start Date", value=date(2000,1,1))
        end_date = col2.date_input("End Date", value=date.today())

        status_filter = st.selectbox("Filter by Status", ["All", "Processing", "Shipped", "Delivered", "Cancelled"])

        # Build base query and params dict
        query = """
            SELECT o.order_id, c.name as customer_name, o.order_date, 
                   o.total_amount, o.current_status, o.discount_id, o.shipping_address_id
            FROM Orders o
            JOIN Customer c ON o.customer_id = c.customer_id
            WHERE 1=1
        """
        params = {}

        # Apply search filter
        if search_term:
            query += " AND (CAST(o.order_id AS TEXT) ILIKE :term OR c.name ILIKE :term)"
            params["term"] = f"%{search_term}%"

        # Apply date filter
        if start_date and end_date:
            query += " AND o.order_date BETWEEN :start_date AND :end_date"
            params["start_date"] = start_date
            params["end_date"] = end_date

        # Apply status filter
        if status_filter != "All":
            query += " AND o.current_status = :status"
            params["status"] = status_filter

        query += " ORDER BY o.order_date DESC"

        orders = conn.execute(text(query), params).fetchall()

        if not orders:
            st.info("No orders found with the selected filters.")
            return

        for order in orders:
            with st.expander(f"Order #{order.order_id} by {order.customer_name} - {order.order_date}"):
                st.write(f"**Total Amount:** ${order.total_amount}")
                st.write(f"**Current Status:** {order.current_status}")

                # --- Editable Order Status ---
                new_status = st.selectbox(
                    "Update Order Status",
                    ["Processing", "Shipped", "Delivered", "Cancelled"],
                    index=["Processing", "Shipped", "Delivered", "Cancelled"].index(order.current_status) if order.current_status in ["Processing", "Shipped", "Delivered", "Cancelled"] else 0,
                    key=f"status_{order.order_id}"
                )
                if st.button("Update Status", key=f"update_status_{order.order_id}"):
                    if new_status != order.current_status:
                        conn.execute(text("""
                            UPDATE Orders SET current_status = :status, updated_at = CURRENT_TIMESTAMP WHERE order_id = :order_id
                        """), {"status": new_status, "order_id": order.order_id})
                        # Insert into order status history
                        conn.execute(text("""
                            INSERT INTO OrderStatusHistory (order_id, status) VALUES (:order_id, :status)
                        """), {"order_id": order.order_id, "status": new_status})
                        st.success(f"Order #{order.order_id} status updated to {new_status}")
                        st.experimental_rerun()

                st.divider()

                # --- Order Items ---
                st.subheader("🛒 Order Items")
                items = conn.execute(text("""
                    SELECT oi.product_id, p.name, oi.quantity, oi.price
                    FROM OrderItem oi
                    JOIN Product p ON oi.product_id = p.product_id
                    WHERE oi.order_id = :order_id
                """), {"order_id": order.order_id}).fetchall()

                for item in items:
                    st.write(f"- **{item.name}** (Qty: {item.quantity}) - ${item.price}")

                st.divider()

                # --- Shipping Address ---
                address = conn.execute(text("""
                    SELECT address, city, state, postal_code, country
                    FROM CustomerAddress
                    WHERE address_id = :addr_id
                """), {"addr_id": order.shipping_address_id}).fetchone()

                if address:
                    st.subheader("📍 Shipping Address")
                    st.write(f"{address.address}, {address.city}, {address.state}, {address.postal_code}, {address.country}")

                st.divider()

                # --- Discount Code ---
                if order.discount_id:
                    discount = conn.execute(text("""
                        SELECT code, description, discount_percent FROM Discount WHERE discount_id = :did
                    """), {"did": order.discount_id}).fetchone()
                    if discount:
                        st.subheader("🏷️ Discount Applied")
                        st.write(f"Code: {discount.code}")
                        st.write(f"Description: {discount.description}")
                        st.write(f"Discount: {discount.discount_percent}%")

                st.divider()

                # --- Order Status History ---
                st.subheader("📜 Status History")
                history = conn.execute(text("""
                    SELECT status, updated_at FROM OrderStatusHistory
                    WHERE order_id = :order_id
                    ORDER BY updated_at DESC
                """), {"order_id": order.order_id}).fetchall()

                for h in history:
                    st.markdown(f"- **{h.status}** at `{h.updated_at}`")

                st.divider()

                # --- Delivery Status ---
                delivery = conn.execute(text("""
                    SELECT status, delivery_date FROM Delivery WHERE order_id = :order_id
                """), {"order_id": order.order_id}).fetchone()

                if delivery:
                    st.subheader("🚚 Delivery Status")
                    st.write(f"Status: {delivery.status}")
                    st.write(f"Delivery Date: {delivery.delivery_date}")

                st.divider()

                # --- Transaction Details ---
                transaction = conn.execute(text("""
                    SELECT amount, status, transaction_date, method FROM Transactions WHERE order_id = :order_id
                """), {"order_id": order.order_id}).fetchone()

                if transaction:
                    st.subheader("💳 Transaction Details")
                    st.write(f"Amount: ${transaction.amount}")
                    st.write(f"Status: {transaction.status}")
                    st.write(f"Date: {transaction.transaction_date}")
                    st.write(f"Method: {transaction.method}")
