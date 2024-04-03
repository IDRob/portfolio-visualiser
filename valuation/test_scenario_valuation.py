import unittest

from marketData import market_id
from marketData.market_data_service import MarketDataService
from path_generators.linear_path import LinearPath
from path_generators.volatile_path import VolatilePath
from portfolio.portfolio import Portfolio
from positions import common_stock
from positions import option
import datetime

from valuation.scenario_valuation import ScenarioValuation


class TestScenarioValuation(unittest.TestCase):

    def test_portfolio_valuation(self):
        security_id = 1
        start_value = 100
        annual_drift = 0.1
        daily_drift = pow(1 + annual_drift, 1 / 255) - 1
        start_date = datetime.datetime(2023, 12, 15, 0, 0)
        end_date = datetime.datetime(2024, 12, 15, 0, 0)
        volatility = 0.2
        number_of_scenarios = 10
        linear_path = LinearPath(daily_value=daily_drift, start_date=start_date, end_date=end_date)
        aaple_path_returns = VolatilePath(volatility=volatility, number_of_paths=number_of_scenarios,
                                          central_path=linear_path)

        market_data_service = MarketDataService()
        market_data_service.add_market_data_from_path(
            path_data_frame=aaple_path_returns.get_cumulative_path(start_value=start_value),
            market_id=market_id.PriceId(security_id=security_id))

        implied_vol_path = LinearPath(daily_value=volatility, start_date=start_date, end_date=end_date)
        implied_vol_scenario_paths = implied_vol_path.repeat_scenarios(number_of_scenarios)

        market_data_service.add_market_data_from_path(
            path_data_frame=implied_vol_scenario_paths.get_path_dataframe(),
            market_id=market_id.VolatilityId(security_id=security_id))

        risk_free_path_scenarios = (LinearPath(daily_value=0.40, start_date=start_date, end_date=end_date)
                                    .repeat_scenarios(number_of_scenarios))

        market_data_service.add_market_data_from_path(
            path_data_frame=risk_free_path_scenarios.get_path_dataframe(),
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

        portfolio_scenario_valuation = ScenarioValuation(
            portfolio=portfolio,
            market_data_service=market_data_service)
        scenario_valuation_dataframe = portfolio_scenario_valuation.get_all_portfolio_valuations()

        self.assertEqual(number_of_scenarios, scenario_valuation_dataframe.shape[1])

    def test_sharpe_ratios(self):
        security_id = 1
        start_value = 100
        annual_drift = 0.1
        daily_drift = pow(1 + annual_drift, 1 / 255) - 1
        start_date = datetime.datetime(2023, 12, 15, 0, 0)
        end_date = datetime.datetime(2024, 12, 15, 0, 0)
        volatility = 0.2
        number_of_scenarios = 10
        linear_path = LinearPath(daily_value=daily_drift, start_date=start_date, end_date=end_date)
        aaple_path_returns = VolatilePath(volatility=volatility, number_of_paths=number_of_scenarios,
                                          central_path=linear_path)

        market_data_service = MarketDataService()
        market_data_service.add_market_data_from_path(
            path_data_frame=aaple_path_returns.get_cumulative_path(start_value=start_value),
            market_id=market_id.PriceId(security_id=security_id))

        implied_vol_path = LinearPath(daily_value=volatility, start_date=start_date, end_date=end_date)
        implied_vol_scenario_paths = implied_vol_path.repeat_scenarios(number_of_scenarios)

        market_data_service.add_market_data_from_path(
            path_data_frame=implied_vol_scenario_paths.get_path_dataframe(),
            market_id=market_id.VolatilityId(security_id=security_id))

        risk_free_path_scenarios = (LinearPath(daily_value=0.04, start_date=start_date, end_date=end_date)
                                    .repeat_scenarios(number_of_scenarios))

        market_data_service.add_market_data_from_path(
            path_data_frame=risk_free_path_scenarios.get_path_dataframe(),
            market_id=market_id.RiskFreeRateId(security_id=security_id))

        portfolio = Portfolio()
        portfolio.add_position(position=option.Option(
            security_id=security_id,
            quantity=1,
            expiry=datetime.datetime(2024, 12, 15, 0, 0),
            strike=120,
            option_type="call"))

        portfolio.add_position(position=option.Option(
            security_id=security_id,
            quantity=1,
            expiry=datetime.datetime(2024, 12, 15, 0, 0),
            strike=100,
            option_type="put"))
        portfolio.add_position(position=common_stock.CommonStock(security_id=security_id, quantity=1))

        portfolio_scenario_valuation = ScenarioValuation(
            portfolio=portfolio,
            market_data_service=market_data_service)
        sharpe_ratios = portfolio_scenario_valuation.get_all_sharpe_ratios(start_date, end_date)
        expected_sharpe_ratios = [
            1.8120537693191332,
            1.401309611659017,
            0.841857859827201,
            3.341559581485809,
            0.08495473304292468,
            -0.7097730482514382,
            -0.4199550278385038,
            -0.3087398075344347,
            3.3887273705379353,
            -0.6439451629693633]

        self.assertEqual(expected_sharpe_ratios, sharpe_ratios)


