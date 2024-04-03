import datetime
import unittest

from marketData.market_data_service import MarketDataService
from marketData.market_id import PriceId
from path_generators.correlated_path import CorrelatedPath
from path_generators.linear_path import LinearPath
from path_generators.volatile_path import VolatilePath


class TestMarketDataService(unittest.TestCase):
    """
    Test Class for Market Data Service Class.
    """
    __start_date = datetime.datetime(2023, 12, 15, 0, 0)
    __end_date = datetime.datetime(2024, 12, 15, 0, 0)

    def test_from_volatile_path(self):
        annual_drift = 0.1
        daily_drift = pow(1 + annual_drift, 1 / 255) - 1
        __linear_path = LinearPath(daily_value=daily_drift, start_date=self.__start_date, end_date=self.__end_date)
        __volatile_path = VolatilePath(volatility=0.2, number_of_paths=1, central_path=__linear_path)
        market_data_service = MarketDataService()
        market_data_service.add_market_data_from_path(
            path_data_frame=__volatile_path.get_cumulative_path(start_value=100.0),
            market_id=PriceId(security_id=1))
        market_data_service_df = market_data_service.get_date_to_market_data()

        # Check that correct number of days market data has been produced.
        self.assertEqual(market_data_service_df.shape[0], 368)

    def test_volatile_and_correlated_path(self):
        annual_drift = 0.1
        daily_drift = pow(1 + annual_drift, 1 / 255) - 1
        __linear_path = LinearPath(daily_value=daily_drift, start_date=self.__start_date, end_date=self.__end_date)
        __volatile_path = VolatilePath(volatility=0.2, number_of_paths=1, central_path=__linear_path)
        __correlated_path = CorrelatedPath(
            correlation=0.8,
            annual_volatility=0.1,
            number_of_paths=1,
            central_path=__volatile_path)
        __cumulative_path_1 = __volatile_path.get_cumulative_path(start_value=100.0)
        __cumulative_path_2 = __correlated_path.get_cumulative_path(start_value=100.0)
        market_data_service = MarketDataService()
        market_data_service.add_market_data_from_path(path_data_frame=__cumulative_path_1,
                                                      market_id=PriceId(security_id=1))
        market_data_service.add_market_data_from_path(path_data_frame=__cumulative_path_2,
                                                      market_id=PriceId(security_id=2))
        market_data_service_dataframe = market_data_service.get_date_to_market_data()
        first_day_market_data = market_data_service_dataframe.iloc[0][0]
        first_day_market_data_dict = first_day_market_data.get_all_market_data()

        # Check that the correct number of days market data is available.
        self.assertEqual(market_data_service_dataframe.shape[0], 368)

        # Check that the right number of pieces of information are available for a given day.
        self.assertEqual(len(first_day_market_data_dict), 2)
