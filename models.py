from dataclasses import dataclass
from datetime import datetime


@dataclass
class PortfileAssetData:
    """Class for keeping track of an Active in porfile."""

    ticker: str
    name: str
    amount: int
    avg_buy_price: int
    date: datetime
    current_price: int
    candels: list

    @property
    def volatility(self):
        pass
  
    @property
    def profit(self):
        pass
