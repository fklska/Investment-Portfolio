from dotenv import load_dotenv

from classes import Markovic

import os
import asyncio

load_dotenv()

TOKEN = os.getenv("TOKEN")

portfel = Markovic(TOKEN)


async def main():
    print(await portfel.get_nessary_data())


if __name__ == "__main__":
    asyncio.run(main())
