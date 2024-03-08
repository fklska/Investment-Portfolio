from tinkoff.invest import Client, AsyncClient, InstrumentIdType, Instrument, GetOperationsByCursorRequest, OperationType, CandleInterval

from datetime import datetime, timedelta

from models import PortfileAssetData

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

    @staticmethod
    def __convert_to_float(amount_value_obj):
        units = amount_value_obj.units
        nano = amount_value_obj.nano

        return float(str(units) + "." + str(nano)[:2])

    async def get_nessary_data(self) -> list[PortfileAssetData]:
        data_storage = []

        async with AsyncClient(self.token) as client:
            acc_request = await client.users.get_accounts()

            for acc in acc_request.accounts:

                request = await client.operations.get_portfolio(account_id=acc.id)
                positions = request.positions

                for item in positions:
                    
                    figi = item.figi
                    quantity = self.__convert_to_float(item.quantity)
                    current_price = self.__convert_to_float(item.current_price)
                    average_price = self.__convert_to_float(item.average_position_price)
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
                            operation_types=[OperationType.OPERATION_TYPE_BUY]
                        )
                    )

                    try:
                        date = instrument_operations.items[0].date
                    except IndexError:
                        date = None

                    historic_data = await client.market_data.get_candles(
                        instrument_id=instrument_uid,
                        from_=datetime.utcnow() - timedelta(days=60),
                        to=datetime.utcnow(),
                        interval=CandleInterval.CANDLE_INTERVAL_MONTH
                    )

                    kwargs = {
                        "ticker": ticker,
                        "name": name,
                        "amount": quantity,
                        "avg_buy_price": average_price,
                        "date": date,
                        "current_price": current_price,
                        "candels": historic_data.candles
                    }

                    data_storage.append(PortfileAssetData(**kwargs))

        return data_storage
