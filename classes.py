from tinkoff.invest import Client, InstrumentIdType, Instrument


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
