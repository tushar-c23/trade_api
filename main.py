from typing import Union
from models import Order
from fastapi import FastAPI, Header
from dhanhq import dhanhq
import httpx

dhanUrl = "https://api.dhan.co"

client_id = "client_id"
access_token = "access_token"

dhan = dhanhq(client_id, access_token)

app = FastAPI()

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
async def place_order_with_tag(order: Order, tag: str):
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
        bo_stop_loss_Value= order.boStopLossValue,
        drv_expiry_date= order.drvExpiryDate,
        drv_options_type= dhan.CALL if order.drvOptionsType == "CALL" else None,
        drv_strike_price= order.drvStrikePrice
    )
    print(resp)
    return resp

@app.post("/orders/")
async def place_order_with_creds(order: Order, dhanClientId: str, correlationId: str, access_token: str):
    order_data = {"dhanClientId": dhanClientId, "correlationId": correlationId, **order.dict()}
    # print("order: ",order_data)
    headers = {'Accept': 'application/json', 'access-token' : access_token}
    url = f"{dhanUrl}/orders"
    resp = httpx.post(url, json=order_data, headers=headers)
    # print(resp.json())
    # return resp
    return resp.json()