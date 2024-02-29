from dotenv import load_dotenv

from classes import Markovic

import os

load_dotenv()

TOKEN = os.getenv("TOKEN")

portfel = Markovic(TOKEN)


def main():
    for i in portfel.get_asset_data():
        print(i.name)
        print(i.ticker)
        print(i.instrument_type)
        print(i.api_trade_available_flag)


if __name__ == "__main__":
    main()
