import logging
from binance.client import Client
from binance.enums import *

BINANCE_ERROR_MESSAGES = {
    -2019: "Margin is insufficient. You don't have enough USDT to place this order. Try reducing your order size or get more testnet funds.",
    -4013: "The price you entered is below the minimum allowed for this trading pair. Please enter a higher price.",
    -4001: "Price cannot be zero or negative. Please enter a valid price.",
}



logging.basicConfig(
    filename='trading_bot.log',
    level=logging.INFO,
    format='%(asctime)s %(levelname)s: %(message)s'
)

class BasicBot:

    def __init__(self, api_key: str, api_secret: str, testnet: bool = True):
        self.client = Client(api_key, api_secret, testnet=testnet)
        self.client.FUTURES_URL = 'https://testnet.binancefuture.com/fapi'
        logging.info("Initialized BasicBot (testnet=%s)", testnet)

    def place_order(self, symbol: str, side: str, order_type: str, quantity: float, price: float = None) -> dict:
        
        try:
            params = {
                'symbol': symbol.upper(),
                'side': side.upper(),
                'type': order_type.upper(),
                'quantity': quantity
            }
            if order_type.upper() == ORDER_TYPE_LIMIT:
                params['price'] = price
                params['timeInForce'] = TIME_IN_FORCE_GTC

            logging.info("Placing order: %s", params)
            order = self.client.futures_create_order(**params)
            logging.info("Order response: %s", order)
            return order

        except Exception as e:
            error_msg = str(e)
            error_code = None
            if "APIError(code=" in error_msg:
                try:
                    error_code = int(error_msg.split("APIError(code=")[1].split(")")[0])
                except Exception:
                    pass

            user_friendly = BINANCE_ERROR_MESSAGES.get(error_code, error_msg)
            logging.error("Order failed: %s", user_friendly)
            return {"error": user_friendly}
