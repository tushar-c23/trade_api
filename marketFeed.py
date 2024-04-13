from dhanhq import marketfeed
import os
from dotenv import load_dotenv

load_dotenv()

client_id = os.getenv("CLIENT_ID")
access_token = os.getenv("ACCESS_TOKEN")

instruments = [(1, "236"),(0,"236")]

subscription_code = marketfeed.Ticker

async def on_connect(instance):
    print("Connected to websocket")

async def on_message(instance, message):
    print("Received: ", message)

print("Subscription Code: ", subscription_code)

feed = await marketfeed.DhanFeed(client_id,
                            access_token,
                            instruments,
                            subscription_code,
                            on_connect=on_connect,
                            on_message=on_message)

feed.run_forever()