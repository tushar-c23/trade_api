from pydantic import BaseModel

class Order(BaseModel):
    tag: str
    transaction_type: str
    exchange_segment: str
    product_type: str
    order_type: str
    validity: str
    security_id: str
    quantity: int
    disclosed_quantity: int
    price: float
    trigger_price: float
    after_market_order: bool = False
    amo_time: str = 'OPEN'
    bo_profit_value: float = 0
    bo_stop_loss_Value: float = 0
    drv_expiry_date: str = None
    drv_options_type: str = None
    drv_strike_price: float = None