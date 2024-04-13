import os
from typing import Union
from models import Order, historicalData
from fastapi import FastAPI, Header
from dhanhq import dhanhq, marketfeed
import httpx
from dotenv import load_dotenv
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.templating import Jinja2Templates
import asyncio

load_dotenv()

dhanUrl = "https://api.dhan.co"

client_id = os.getenv("CLIENT_ID")
access_token = os.getenv("ACCESS_TOKEN")

dhan = dhanhq(client_id, access_token)

app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.get("/")
def read_root():
    return { "Hello Trader!" }

@app.get("/myHoldings")
async def get_my_holdings():
    return dhan.get_holdings()

@app.get("/myPositions")
async def get_my_positions():
    return dhan.get_positions()

@app.get("/holdings")
async def get_holdings(access_token: str):
    if access_token:
        headers = {'Accept': 'application/json', 'access-token' : access_token}
        url = f"{dhanUrl}/holdings"
        fetcehed_holdings = httpx.get(url, headers=headers)
        return fetcehed_holdings.json()

@app.get("/positions")
async def get_positions(access_token: str):
    if access_token:
        headers = {'Accept': 'application/json', 'access-token' : access_token}
        url = f"{dhanUrl}/positions"
        fetcehed_positions = httpx.get(url, headers=headers)
        return fetcehed_positions.json()

#TODO: Refactoring and adding more params ideally divert this to another function
@app.post("/myOrders/")
async def place_order_with_tag(order: Order, tag: str | None = None):
    resp = None
    if (order.exchangeSegment == "NSE_FNO" or order.exchangeSegment == "BSE_FNO"):
        resp = dhan.place_order(
            tag=tag,
            transaction_type= dhan.SELL if order.transactionType == "SELL" else dhan.BUY,
            exchange_segment= dhan.NSE_FNO if order.exchangeSegment == "NSE_FNO" else dhan.BSE_FNO,
            product_type= dhan.INTRA if order.productType == "INTRADAY" else dhan.CNC,
            order_type= dhan.LIMIT if order.orderType == "LIMIT" else dhan.MARKET,
            validity= dhan.DAY if order.validity == "DAY" else dhan.IOC,
            security_id= order.securityId,
            quantity= order.quantity,
            disclosed_quantity= order.disclosedQuantity,
            price= order.price,
            trigger_price= order.triggerPrice,
            after_market_order= order.afterMarketOrder,
            amo_time= order.amoTime,
            bo_profit_value= order.boProfitValue,
            bo_stop_loss_Value= order.boStopLossValue,
            drv_expiry_date= order.drvExpiryDate,
            drv_options_type= dhan.CALL if order.drvOptionsType == "CALL" else None,
            drv_strike_price= order.drvStrikePrice
        )
    else:
        resp = dhan.place_order(
            tag=tag,
            transaction_type= dhan.SELL if order.transactionType == "SELL" else dhan.BUY,
            exchange_segment= dhan.NSE if order.exchangeSegment == "NSE_EQ" else dhan.BSE,
            product_type= dhan.INTRA if order.productType == "INTRADAY" else dhan.CNC,
            order_type= dhan.LIMIT if order.orderType == "LIMIT" else dhan.MARKET,
            validity= dhan.DAY if order.validity == "DAY" else dhan.IOC,
            security_id= order.securityId,
            quantity= order.quantity,
            disclosed_quantity= order.disclosedQuantity,
            price= order.price,
            trigger_price= order.triggerPrice,
            after_market_order= order.afterMarketOrder,
            amo_time= order.amoTime,
            bo_profit_value= order.boProfitValue,
            bo_stop_loss_Value= order.boStopLossValue
        )
    print(resp)
    return resp

@app.post("/orders/")
async def place_order_with_creds(order: Order, dhanClientId: str, access_token: str, correlationId: str | None = None):
    order_data = {}
    if correlationId is None:
        order_data = {"dhanClientId": dhanClientId, **order.dict()}   
    else: 
        order_data = {"dhanClientId": dhanClientId, "correlationId": correlationId, **order.dict()}

    headers = {'Accept': 'application/json', 'access-token' : access_token}
    url = f"{dhanUrl}/orders"
    resp = httpx.post(url, json=order_data, headers=headers)
    
    return resp.json()

@app.post("/historicalData/")
async def get_historical_data(historicalData: historicalData, access_token: str | None):
    if(access_token):
        headers = {'Accept': 'application/json', 'access-token' : access_token}
        url = f"{dhanUrl}/charts/historical"
        fetched_data = httpx.post(url, json=historicalData.dict(), headers=headers)
        return fetched_data.json()

@app.post("/historicalDataPy/")
async def get_historical_data_with_python(historicalData: historicalData):
    fetched_data = dhan.historical_daily_data(
        symbol=historicalData.symbol,
        exchange_segment=historicalData.exchangeSegment,
        instrument_type=historicalData.instrument,
        expiry_code=historicalData.expiryCode,
        from_date=historicalData.fromDate,
        to_date=historicalData.toDate
    )
    return fetched_data

@app.get("/marketFeed/")
async def get_market_feed():
    instruments = [(1, "236"),(0,"236")]
    subscription_code = marketfeed.Ticker
    async def on_connect(instance):
        print("Connected to websocket")
    async def on_message(instance, message):
        return message
        print("Received: ", message)
    feed = marketfeed.DhanFeed(client_id,
                                access_token,
                                instruments,
                                subscription_code,
                                on_connect=on_connect,
                                on_message=on_message)
    # feed.run_forever()
    asyncio.get_event_loop().create_task(feed.connect())

@app.get("/testPostback")
async def test_postback():
    url = "https://dhan-postback-handler.onrender.com/postback"
    testData = {
        "dhanClientId": "1000000003",
        "orderId": "112111182198",
        "correlationId":"123abc678",
        "orderStatus": "PENDING",
        "transactionType": "BUY",
        "exchangeSegment": "NSE_EQ",
        "productType": "INTRADAY",
        "orderType": "MARKET",
        "validity": "DAY",
        "tradingSymbol": "",
        "securityId": "11536",
        "quantity": 5,
        "disclosedQuantity": 0,
        "price": 0.0,
        "triggerPrice": 0.0,
        "afterMarketOrder": False,
        "boProfitValue": 0.0,
        "boStopLossValue": 0.0,
        "legName": "",
        "createTime": "2021-11-24 13:33:03",
        "updateTime": "2021-11-24 13:33:03",
        "exchangeTime": "2021-11-24 13:33:03",
        "drvExpiryDate": None,
        "drvOptionType": None,
        "drvStrikePrice": 0.0,
        "omsErrorCode": None,
        "omsErrorDescription": None
    }
    fetched_data = httpx.post(url, json=testData)
    return fetched_data.json()