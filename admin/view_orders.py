import streamlit as st
from sqlalchemy import text
from db.connection import get_engine

def view_orders():
    st.title("📦 View Customer Orders")

    engine = get_engine()
    with engine.begin() as conn:
        # Fetch all orders
        query = text("""
            SELECT o.order_id, c.name as customer_name, o.order_date, 
                   o.total_amount, o.current_status
            FROM Orders o
            JOIN Customer c ON o.customer_id = c.customer_id
            ORDER BY o.order_date DESC
        """)
        orders = conn.execute(query).fetchall()

        if not orders:
            st.info("No orders found.")
            return

        for order in orders:
            with st.expander(f"Order #{order.order_id} - {order.customer_name}"):
                st.write(f"📅 **Date:** `{order.order_date}`")
                st.write(f"💰 **Total Amount:** `${order.total_amount}`")
                st.write(f"🚚 **Current Status:** `{order.current_status}`")

                # Order items
                item_query = text("""
                    SELECT p.name AS product_name, oi.quantity, oi.price
                    FROM OrderItem oi
                    JOIN Product p ON oi.product_id = p.product_id
                    WHERE oi.order_id = :order_id
                """)
                items = conn.execute(item_query, {"order_id": order.order_id}).fetchall()

                st.write("### 🛒 Ordered Items")
                for item in items:
                    st.markdown(f"- **{item.product_name}** | Quantity: `{item.quantity}` | Price: `${item.price}`")

                # Update order status
                st.write("### ✏️ Update Order Status")
                new_status = st.selectbox(
                    "Select new status",
                    ["Processing", "Shipped", "Delivered", "Cancelled"],
                    index=["Processing", "Shipped", "Delivered", "Cancelled"].index(order.current_status) if order.current_status in ["Processing", "Shipped", "Delivered", "Cancelled"] else 0,
                    key=f"status_{order.order_id}"
                )

                if st.button(f"✅ Update Status for Order #{order.order_id}"):
                    conn.execute(text("""
                        UPDATE Orders SET current_status = :status WHERE order_id = :order_id
                    """), {"status": new_status, "order_id": order.order_id})

                    # Save to order history
                    conn.execute(text("""
                        INSERT INTO OrderStatusHistory (order_id, status)
                        VALUES (:order_id, :status)
                    """), {"order_id": order.order_id, "status": new_status})

                    st.success(f"Order #{order.order_id} status updated to '{new_status}'! Please refresh.")
