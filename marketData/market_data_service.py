import copy

import pandas as pd

from marketData.market_data import MarketData


class MarketDataService:
    """ Market Data Service Class
    Holds market data for each date.
    """

    def __init__(self):
        """
        Initialize Market Data Service class.
        """
        self.__date_to_market_data = {}

    def add_market_data(self, *, market_data):
        """
        Adds Market Data to the Market Data Service.

        :param market_data: MarketData
        :return: none
        """
        if isinstance(market_data, MarketData):
            date = market_data.get_date()
            if date in self.__date_to_market_data:
                existing_market_data = self.__date_to_market_data[date]
                existing_market_data.add_all_market_data(market_data=market_data)
            else:
                self.__date_to_market_data[date] = market_data
        else:
            raise ValueError("")

    def add_market_data_from_path(self, *, path_data_frame, market_id):
        """
        Adds the market data from a path generator.

        :param path_data_frame: Path
        :param market_id: MarketId
        :return: none
        """
        if isinstance(path_data_frame, pd.DataFrame):
            for date, row in path_data_frame.iterrows():
                data = MarketData(date=date)
                data.add_market_data(key=market_id, value=row)
                self.add_market_data(market_data=data)
        else:
            raise ValueError()

    def get_date_to_market_data(self):
        """
        Gets the dataframe with index as date and values as the market data.

        :return: dataframe
        """
        return copy.deepcopy(pd.DataFrame.from_dict(self.__date_to_market_data, orient='index'))

    def get_number_scenarios(self, *, market_id):
        """
        Gets the minimum number of scenarios in the market data for a given market id for all dates.

        If on one date there are six scenarios and on another date there are three, the minimum value three will be
        returned.

        Parameters
        ----------
        market_id: MarketId

        Returns int
        -------

        """
        number_of_scenarios = []
        for date, row in self.get_date_to_market_data().iterrows():
            scenarios = row[0].get_number_scenarios(market_id=market_id)
            number_of_scenarios.append(scenarios)

        return min(number_of_scenarios)


