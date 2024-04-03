from securities import financial_security


class Equity(financial_security.Security):
    def __init__(self, *, security_id):
        super().__init__(security_id=security_id)
