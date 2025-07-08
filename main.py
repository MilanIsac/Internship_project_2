import streamlit as st
from bot import BasicBot

order = None

st.title("Binance Futures Testnet Trading Bot")

st.sidebar.header("API Credentials")
api_key = st.sidebar.text_input("API Key", type="password")
api_secret = st.sidebar.text_input("API Secret", type="password")

with st.form("order_form"):
    st.subheader("Place an Order")
    symbol = st.text_input("Symbol (e.g., BTCUSDT)", value="BTCUSDT")
    side = st.selectbox("Side", ["BUY", "SELL"])
    order_type = st.selectbox("Order Type", ["MARKET", "LIMIT"])
    quantity = st.number_input("Quantity", min_value=0.001, value=0.001)
    price = None
    if order_type == "LIMIT":
        price = st.number_input("Limit Price", min_value=0.0, value=0.0)
    submit = st.form_submit_button("Submit Order")

if submit:
    if not api_key or not api_secret:
        st.error("Please enter your API credentials in the sidebar.")
    else:
        bot = BasicBot(api_key, api_secret, testnet=True)
        order = bot.place_order(
            symbol=symbol,
            side=side,
            order_type=order_type,
            quantity=quantity,
            price=price if order_type == "LIMIT" else None
        )
        if order and "error" not in order:
            # st.json(order)
            if "orderId" in order:
                st.success("Order placed successfully!")
                st.markdown(f"""
                **Order ID:** `{order.get('orderId')}`  
                **Symbol:** `{order.get('symbol')}`  
                **Side:** `{order.get('side')}`  
                **Type:** `{order.get('type')}`  
                **Status:** `{order.get('status')}`  
                **Quantity:** `{order.get('origQty')}`  
                **Price:** `{order.get('price')}`  
                """)
            else:
                st.error("Order placed, but no order details returned.")

        else:
            error_msg = order.get('error', 'Unknown error') if order else 'Order failed. Unknown error.'
            st.error(f"Order failed: {error_msg}")

if st.checkbox("Show Log"):
    try:
        with open("trading_bot.log") as log_file:
            st.text(log_file.read())
    except FileNotFoundError:
        st.info("No log file found yet.")
