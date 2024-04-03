from positions import financial_position
from securities import equity


class CommonStock(financial_position.Position):
    def __init__(self, *, security_id, quantity):
        security = equity.Equity(security_id=security_id)
        super().__init__(security=security, quantity=quantity)

    def get_type(self):
        return 'common stock'
