from dhanhq import marketfeed

client_id = 'your_client_id'
access_token = 'your_access_token'

instruments = [(1, "1334"),(0,"13")]

subscription_code = marketfeed.Ticker

async def on_connect(instance):
    print("Connected to websocket")

async def on_message(instance, message):
    print("Received: ", message)

print("Subscription Code: ", subscription_code)

feed = marketfeed.DhanFeed(client_id,
                            access_token,
                            instruments,
                            subscription_code,
                            on_connect=on_connect,
                            on_message=on_message)

feed.run_forever()