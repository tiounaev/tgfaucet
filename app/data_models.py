from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel

class ParamSettings(BaseModel):
    sub_price: float
    sub_price_percent: float
    join_price: float
    join_price_percent: float
    view_price: float
    view_price_percent: float
    mult_view_price: float
    multi_view_price_percent: float
