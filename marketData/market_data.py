import copy


class MarketData:
    """Market Data Class
    Holds all market data for a specific date
    """

    def __init__(self, *, date):
        """
        Initialize Market Data Class for give date

        :param date: datetime
        """
        self.__date = copy.deepcopy(date)
        self.__market_data = {}

    def add_market_data(self, *, key, value):
        """
        Adds market value which matches instance type for data key

        :param key: MarketId
        :param value: any
        :return: none
        """

        if [isinstance(v, key.instance_type) for v in value]:
            self.__market_data[copy.deepcopy(key)] = copy.deepcopy(value)
        else:
            raise ValueError("Value {} is not instance type {}".format(value, key.instance_type))

    def add_all_market_data(self, *, market_data):
        """
        Adds MarketData

        :param market_data: MarketData
        :return: none
        """
        if isinstance(market_data, MarketData):
            for key in market_data.get_all_market_data():
                self.add_market_data(key=key, value=market_data.get_all_market_data()[key])
        else:
            raise ValueError("Must be of type {} but was {}".format(MarketData, market_data))

    def get_market_data(self, *, market_id, scenario_number):
        """
        Get market data value for given market data id

        :param scenario_number:
        :param market_id: MarketId
        :return: any
        """
        data = copy.deepcopy(self.__market_data[market_id][scenario_number])
        return data

    def get_number_scenarios(self, *, market_id):
        """
        Gets the number of scenarios in the market data for a given market id.

        Parameters
        ----------
        market_id: MarketId

        Returns int
        -------

        """
        data = self.__market_data[market_id]
        return len(data)

    def get_all_market_data(self):
        """
        Gets all market data

        :return: MarketData
        """
        return copy.deepcopy(self.__market_data)

    def get_date(self):
        """
        Gets date of market data

        :return: datetime
        """
        return copy.deepcopy(self.__date)
