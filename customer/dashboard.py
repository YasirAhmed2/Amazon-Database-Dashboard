import streamlit as st
from db import get_connection

def customer_dashboard():
    st.title("Welcome to Customer Dashboard")
    st.markdown(f"Logged in as: `{st.session_state.customer_id}`")

    menu = ["My Orders", "Browse Products", "Place Order", "Update Profile", "Logout"]
    choice = st.selectbox("Menu", menu)

    conn = get_connection()
    cur = conn.cursor()

    if choice == "My Orders":
        st.subheader("Your Orders")
        try:
            cur.execute("SELECT * FROM orders WHERE customer_id = %s ORDER BY order_date DESC", (st.session_state.customer_id,))
            orders = cur.fetchall()
            if not orders:
                st.info("No orders found.")
            else:
                for order in orders:
                    order_dict = dict(zip([desc[0] for desc in cur.description], order))
                    st.markdown(f"**Order ID:** {order_dict['order_id']} - Date: {order_dict['order_date']}")
                    st.write(f"Status: {order_dict.get('status', 'N/A')}")
                    st.write(f"Total: {order_dict.get('total_amount', 'N/A')} PKR")
                    st.markdown("---")
        except Exception as e:
            st.error(f"Error fetching orders: {e}")

    elif choice == "Browse Products":
        st.subheader("Product Catalog")
        try:
            cur.execute("SELECT product_id, name, price, description FROM product LIMIT 100")
            rows = cur.fetchall()
            if not rows:
                st.info("No products available.")
            else:
                for row in rows:
                    row_dict = dict(zip([desc[0] for desc in cur.description], row))
                    st.markdown(f"### {row_dict['name']} - {row_dict['price']} PKR")
                    st.write(row_dict.get("description", "No description available"))
                    st.markdown("---")
        except Exception as e:
            st.error(f"Error fetching products: {e}")

    elif choice == "Place Order":
        st.subheader("Place a New Order")
        try:
            # Fetch products for ordering
            cur.execute("SELECT product_id, name, price FROM product LIMIT 100")
            products = cur.fetchall()
            if not products:
                st.info("No products available for ordering.")
            else:
                product_dict = {str(p[0]): (p[1], p[2]) for p in products}  # id: (name, price)
                selected_product_id = st.selectbox(
                    "Select a product to order",
                    options=list(product_dict.keys()),
                    format_func=lambda x: f"{product_dict[x][0]} - {product_dict[x][1]} PKR"
                )
                quantity = st.number_input("Quantity", min_value=1, max_value=100, value=1)

                if st.button("Add to Cart"):
                    if "cart" not in st.session_state:
                        st.session_state.cart = {}
                    cart = st.session_state.cart

                    if selected_product_id in cart:
                        cart[selected_product_id] += quantity
                    else:
                        cart[selected_product_id] = quantity

                    st.success(f"Added {quantity} x {product_dict[selected_product_id][0]} to cart.")

                # Show current cart and option to checkout
                if "cart" in st.session_state and st.session_state.cart:
                    st.markdown("### Your Cart")
                    total_amount = 0
                    for pid, qty in st.session_state.cart.items():
                        pname, price = product_dict[pid]
                        st.write(f"{pname} x {qty} = {qty * price} PKR")
                        total_amount += qty * price
                    st.write(f"**Total Amount: {total_amount} PKR**")

                    if st.button("Place Order"):
                        try:
                            # Create new order record
                            cur.execute(
                                "INSERT INTO orders (customer_id, order_date, current_status, total_amount) VALUES (%s, NOW(), %s, %s) RETURNING order_id",
                                (st.session_state.customer_id, "Pending", total_amount)
                            )
                            order_id = cur.fetchone()[0]

                            # Insert order items
                            for pid, qty in st.session_state.cart.items():
                                cur.execute(
                                    "INSERT INTO orderitem (order_id, product_id, quantity,price) VALUES (%s, %s, %s,%s)",
                                    (order_id, int(pid), qty,total_amount)
                                )

                            conn.commit()
                            st.success("Order placed successfully!")
                            st.session_state.cart = {}  # clear cart
                        except Exception as e:
                            conn.rollback()
                            st.error(f"Failed to place order: {e}")
        except Exception as e:
            st.error(f"Error during order placement: {e}")



    elif choice == "Logout":
        st.session_state.clear()
        st.rerun()

    cur.close()
    conn.close()
