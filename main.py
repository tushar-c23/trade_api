from dhanhq import dhanhq
from dhanhq import marketfeed

client_id = "client_id"
access_token = "access_token"

dhan = dhanhq(client_id, access_token)

# Order place buy
dhan.place_order(security_id='1333', #hdfcBank
                exchange_segment=dhan.NSE,
                transaction_type=dhan.BUY,
                quantity=1,
                order_type=dhan.MARKET,
                product_type=dhan.INTRA,
                price=0)

#Order place sell
dhan.place_order(security_id='1333', #hdfcBank
                exchange_segment=dhan.NSE,
                transaction_type=dhan.SELL,
                quantity=1,
                order_type=dhan.MARKET,
                product_type=dhan.INTRA,
                price=0)

# Get all orders
dhan.get_order_list()

# Get holdings
dhan.get_holdings()

instruments = [(1, "1333"), (0, "11536")]

subscription_code = marketfeed.Ticker

async def on_connect(instance):
    print("Connected to the server")

async def on_message(isntance, message):
    print("Message: ", message)

print("Subscription code :", subscription_code)

feed = marketfeed.DhanFeed(client_id,
                            access_token,
                            instruments,
                            subscription_code,
                            on_connect=on_connect,
                            on_message=on_message)

feed.run_forever()