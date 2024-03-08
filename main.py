from dotenv import load_dotenv

from classes import Markovic
from models import PortfileAssetData

import os
import asyncio

load_dotenv()

TOKEN = os.getenv("TOKEN")

portfel = Markovic(TOKEN)


async def main():
    data = await portfel.get_nessary_data()
    print(data[0].volatility)


if __name__ == "__main__":
    #test_active = PortfileAssetData(
    #    "TEST",
    #    "TEST",
    #    2,
    #    4649,
    #    None,
    #    current_price=7523,
    #    candels=[],
    #)
    #print(test_active.profit)
    asyncio.run(main())
