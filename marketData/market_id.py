class MarketId:
    """ Market Id Class
    Keys used to lookup pieces of market information from MarketData objects.
    """
    def __init__(self, *, market_type, security_id, instance_type):
        """
        Initialize Market Id Class.

        :param market_type: str
        :param security_id: any
        :param instance_type: float
        """
        self.market_type = market_type
        self.security_id = security_id
        self.instance_type = instance_type

    def __hash__(self):
        return hash((self.market_type, self.security_id, self.instance_type))

    def __eq__(self, other):
        return (self.market_type, self.security_id, self.instance_type) == (other.market_type, other.security_id, self.instance_type)


class VolatilityId(MarketId):
    """ Volatility Id Class
    Key used to lookup volatility market data.
    """
    def __init__(self, *, security_id):
        """
        Initialize the Volatility Id Class.

        :param security_id: any
        """
        super().__init__(market_type="volatility", security_id=security_id, instance_type=float)


class RiskFreeRateId(MarketId):
    """ Risk Free Rate Id Class
    Key used to lookup risk free rate market data.
    """
    def __init__(self, *, security_id):
        """
        Initialize the Risk Free Rate Id Class.

        :param security_id: any
        """
        super().__init__(market_type="risk_free_rate", security_id=security_id, instance_type=float)


class PriceId(MarketId):
    """ PriceId Class
    Key used to lookup price market data.
    """
    def __init__(self, *, security_id):
        """
        Initialize the Price Id Class.

        :param security_id: any
        """
        super().__init__(market_type="price", security_id=security_id, instance_type=float)


