from typing import Union

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