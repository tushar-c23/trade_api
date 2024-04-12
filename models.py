from pydantic import BaseModel

class Order(BaseModel):
    transactionType: str
    exchangeSegment: str
    productType: str
    orderType: str
    validity: str
    tradingSymbol: str | None = None
    securityId: str
    quantity: int
    disclosedQuantity: int
    price: float
    triggerPrice: float
    afterMarketOrder: bool = False
    amoTime: str = 'OPEN'
    boProfitValue: float = 0
    boStopLossValue: float = 0
    drvExpiryDate: str = None
    drvOptionsType: str = None
    drvStrikePrice: float = None
