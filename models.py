from dataclasses import dataclass
from datetime import datetime

@dataclass
class SimpleCandle:
    _open: int
    close: int

@dataclass
class PortfileAssetData:
    """Class for keeping track of an Active in porfile."""

    ticker: str
    name: str
    amount: int
    avg_buy_price: int
    date: datetime
    current_price: int
    candels: list[SimpleCandle]

    @property
    def volatility(self):
        volatility = 0
        for candle in self.candels:
            volatility += round(100 * (candle.close - candle._open) / candle._open, 2)

        return round(volatility / len(self.candels), 2)

    @property
    def profit(self):
        return round(100 * (self.current_price - self.avg_buy_price) / self.avg_buy_price , 2)
    
