from tinkoff.invest import Client, AsyncClient, InstrumentIdType, Instrument, GetOperationsByCursorRequest, OperationType, CandleInterval

from datetime import datetime, timedelta

class Markovic:
    def __init__(self, token) -> None:
        self.token = token

    def get_asset_data(self) -> list[Instrument]:
        data = []
        with Client(self.token) as client:
            request = client.users.get_accounts().accounts

            for account in request:
                actives = client.operations.get_positions(
                    account_id=account.id
                ).securities

                for active in actives:
                    data.append(
                        client.instruments.get_instrument_by(
                            id_type=InstrumentIdType.INSTRUMENT_ID_TYPE_FIGI,
                            id=active.figi
                        ).instrument
                    )

            return data

    async def get_nessary_data(self):
        async with AsyncClient(self.token) as client:
            acc_request = await client.users.get_accounts()

            for acc in acc_request.accounts:

                request = await client.operations.get_portfolio(account_id=acc.id)
                positions = request.positions

                for item in positions:

                    figi = item.figi
                    quantity = item.quantity
                    current_price = item.current_price
                    average_price = item.average_position_price
                    instrument_uid = item.instrument_uid

                    instrument = await client.instruments.get_instrument_by(
                        id_type=InstrumentIdType.INSTRUMENT_ID_TYPE_UID,
                        id=instrument_uid
                        )

                    ticker = instrument.instrument.ticker
                    name = instrument.instrument.name

                    instrument_operations = await client.operations.get_operations_by_cursor(
                        GetOperationsByCursorRequest(
                            account_id=acc.id,
                            instrument_id=instrument_uid,
                        )
                    )

                    date = instrument_operations.items.count

                    historic_data = await client.market_data.get_candles(
                        instrument_id=instrument_uid,
                        from_=datetime.utcnow() - timedelta(days=60),
                        to=datetime.utcnow(),
                        interval=CandleInterval.CANDLE_INTERVAL_MONTH
                    )

        return {
            "Ticker": ticker,
            "Name": name,
            "Amount": quantity,
            "Buy_price_avg": average_price,
            "Date": date,
            "Current_price": current_price,
            "Candels_data": historic_data.candles
        }
