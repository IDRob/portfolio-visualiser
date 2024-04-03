import unittest

from pyblackscholesanalytics.market.market import MarketEnvironment

import portfolio_valuation
from marketData import market_data
from marketData import market_id
from marketData.market_data_service import MarketDataService
from path_generators.linear_path import LinearPath
from path_generators.volatile_path import VolatilePath
from portfolio.portfolio import Portfolio
from positions import common_stock
from positions import option
import datetime


class TestPortfolioValuation(unittest.TestCase):

    def test_common_stock(self):
        valuation_date = datetime.datetime(2023, 12, 15, 0, 0)
        security_id = 1
        security_market_data = market_data.MarketData(date=valuation_date)
        security_market_data.add_market_data(key=market_id.PriceId(security_id=security_id), value=[1.1])
        security = common_stock.CommonStock(security_id=security_id, quantity=100)
        present_value = portfolio_valuation.present_value(
            mkt_env=MarketEnvironment(),
            position_to_value=security,
            market_data=security_market_data,
            scenario_number=0)
        self.assertAlmostEqual(present_value, 110, 5)

    def test_option(self):
        valuation_date = datetime.datetime(2023, 12, 15, 0, 0)
        security_id = 1
        security_market_data = market_data.MarketData(date=valuation_date)
        security_market_data.add_market_data(key=market_id.PriceId(security_id=security_id), value=[1.1])
        security_market_data.add_market_data(key=market_id.VolatilityId(security_id=security_id), value=[0.5])
        security_market_data.add_market_data(key=market_id.RiskFreeRateId(security_id=security_id), value=[0.05])

        quantity = 1
        expiry = datetime.datetime(2024, 1, 15, 0, 0)
        strike = 1.2
        option_type = "call"
        security = option.Option(
            security_id=security_id,
            quantity=quantity,
            expiry=expiry,
            strike=strike,
            option_type=option_type)

        present_value = portfolio_valuation.present_value(
            mkt_env=MarketEnvironment(),
            position_to_value=security,
            market_data=security_market_data,
            scenario_number=0)

        self.assertAlmostEqual(present_value, 0.029631, 5)

    def test_expired_option(self):
        valuation_date = datetime.datetime(2025, 12, 15, 0, 0)
        security_id = 1
        security_market_data = market_data.MarketData(date=valuation_date)
        security_market_data.add_market_data(key=market_id.PriceId(security_id=security_id), value=[1.1])
        security_market_data.add_market_data(key=market_id.VolatilityId(security_id=security_id), value=[0.5])
        security_market_data.add_market_data(key=market_id.RiskFreeRateId(security_id=security_id), value=[0.05])

        quantity = 1
        expiry = datetime.datetime(2024, 1, 15, 0, 0)
        strike = 1.0
        option_type = "call"
        security = option.Option(
            security_id=security_id,
            quantity=quantity,
            expiry=expiry,
            strike=strike,
            option_type=option_type)

        present_value = portfolio_valuation.present_value(
            mkt_env=MarketEnvironment(),
            position_to_value=security,
            market_data=security_market_data,
            scenario_number=0)

        self.assertEqual(present_value, None, 5)

    def test_portfolio_present_value(self):
        security_id = 1
        valuation_date = datetime.datetime(2023, 12, 15, 0, 0)
        security_market_data = market_data.MarketData(date=valuation_date)
        security_market_data.add_market_data(key=market_id.PriceId(security_id=security_id), value=[1.1])
        security_market_data.add_market_data(key=market_id.VolatilityId(security_id=security_id), value=[0.5])
        security_market_data.add_market_data(key=market_id.RiskFreeRateId(security_id=security_id), value=[0.05])

        quantity = 1
        expiry = datetime.datetime(2024, 1, 15, 0, 0)
        strike = 1.2
        option_type = "call"

        portfolio = Portfolio()
        portfolio.add_position(position=option.Option(
            security_id=security_id,
            quantity=quantity,
            expiry=expiry,
            strike=strike,
            option_type=option_type))
        portfolio.add_position(position=common_stock.CommonStock(security_id=security_id, quantity=100))

        present_value = portfolio_valuation.portfolio_present_value(
            mkt_env=MarketEnvironment(),
            portfolio=portfolio,
            market_data=security_market_data,
            scenario_number=0)

        self.assertAlmostEqual(present_value, [0.0296318319765842, 110.00000000000001], 5)

    def test_portfolio_valuation(self):
        security_id = "AAPL"
        start_value = 1000
        annual_drift = 0.1
        daily_drift = pow(1 + annual_drift, 1 / 255) - 1
        start_date = datetime.datetime(2023, 12, 15, 0, 0)
        end_date = datetime.datetime(2024, 12, 15, 0, 0)
        volatility = 0.2
        linear_path = LinearPath(daily_value=daily_drift, start_date=start_date, end_date=end_date)
        aaple_path_returns = VolatilePath(volatility=volatility, number_of_paths=1, central_path=linear_path)

        market_data_service = MarketDataService()
        market_data_service.add_market_data_from_path(
            path_data_frame=aaple_path_returns.get_cumulative_path(start_value=start_value),
            market_id=market_id.PriceId(security_id=security_id))

        implied_vol_path = LinearPath(daily_value=volatility, start_date=start_date, end_date=end_date)

        market_data_service.add_market_data_from_path(
            path_data_frame=implied_vol_path.get_path_dataframe(),
            market_id=market_id.VolatilityId(security_id=security_id))

        risk_free_path = LinearPath(daily_value=0.40, start_date=start_date, end_date=end_date)

        market_data_service.add_market_data_from_path(
            path_data_frame=risk_free_path.get_path_dataframe(),
            market_id=market_id.RiskFreeRateId(security_id=security_id))

        portfolio = Portfolio()
        portfolio.add_position(position=option.Option(
            security_id=security_id,
            quantity=1,
            expiry=datetime.datetime(2024, 12, 15, 0, 0),
            strike=1200,
            option_type="call"))

        portfolio.add_position(position=option.Option(
            security_id=security_id,
            quantity=1,
            expiry=datetime.datetime(2024, 12, 15, 0, 0),
            strike=1000,
            option_type="put"))
        portfolio.add_position(position=common_stock.CommonStock(security_id=security_id, quantity=1))

        __portfolio_valuation = portfolio_valuation.PortfolioValuation(
            portfolio=portfolio,
            market_data_service=market_data_service,
            scenario_number=0)

        self.assertAlmostEqual(__portfolio_valuation.get_portfolio_securities_valuation().shape[1], 3, 5)

    def test_portfolio_valuation_expired_option(self):
        security_id = "AAPL"
        start_value = 1000
        annual_drift = 0.1
        daily_drift = pow(1 + annual_drift, 1 / 255) - 1
        start_date = datetime.datetime(2023, 12, 15, 0, 0)
        end_date = datetime.datetime(2024, 12, 15, 0, 0)
        volatility = 0.2
        linear_path = LinearPath(daily_value=daily_drift, start_date=start_date, end_date=end_date)
        aaple_path_returns = VolatilePath(volatility=volatility, number_of_paths=1, central_path=linear_path)

        market_data_service = MarketDataService()
        market_data_service.add_market_data_from_path(
            path_data_frame=aaple_path_returns.get_cumulative_path(start_value=start_value),
            market_id=market_id.PriceId(security_id=security_id))

        implied_vol_path = LinearPath(daily_value=volatility, start_date=start_date, end_date=end_date)

        market_data_service.add_market_data_from_path(
            path_data_frame=implied_vol_path.get_path_dataframe(),
            market_id=market_id.VolatilityId(security_id=security_id))

        risk_free_path = LinearPath(daily_value=0.40, start_date=start_date, end_date=end_date)

        market_data_service.add_market_data_from_path(
            path_data_frame=risk_free_path.get_path_dataframe(),
            market_id=market_id.RiskFreeRateId(security_id=security_id))

        portfolio = Portfolio()
        portfolio.add_position(position=option.Option(
            security_id=security_id,
            quantity=1,
            expiry=datetime.datetime(2024, 6, 15, 0, 0),
            strike=1200,
            option_type="call"))

        __portfolio_valuation = portfolio_valuation.PortfolioValuation(
            portfolio=portfolio,
            market_data_service=market_data_service,
            scenario_number=0)

        self.assertFalse(__portfolio_valuation.get_portfolio_valuation().isnull().values.any())
