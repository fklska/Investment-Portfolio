from dotenv import load_dotenv

from classes import Markovic

import os
import asyncio

load_dotenv()

TOKEN = os.getenv("TOKEN")

portfel = Markovic(TOKEN)


async def main():
    data = await portfel.get_nessary_data()
    print(data[0].date)


if __name__ == "__main__":
    asyncio.run(main())
