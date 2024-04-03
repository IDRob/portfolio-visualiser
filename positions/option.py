from datetime import datetime

from positions import financial_position
from securities import equity


class Option(financial_position.Position):
    """ General Option Class

    Attributes
    ==========
    expiry: instance of datetime
    strike: double
    option_type:

    """

    def __init__(self, *, security_id, quantity, expiry, strike, option_type):
        """
        Initialise an Option

        :param security_id: int
        :param quantity: int
        :param expiry: instance of datetime
        :param strike: float
        :param option_type: str
        """
        security = equity.Equity(security_id=security_id)
        super().__init__(security=security, quantity=quantity)
        self.expiry = expiry
        self.strike = strike
        self.option_type = option_type

    def get_type(self):
        return self.option_type
