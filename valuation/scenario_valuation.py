import pandas as pd

from marketData.market_data_service import MarketDataService

from valuation import portfolio_valuation


class ScenarioValuation:
    """ Scenario Valuation Class
    Performs multiple scenario valuation on a given portfolio.
    """

    def __init__(self, *, portfolio, market_data_service: MarketDataService):
        """
        Initialize the Scenario Valuation Class.

        Parameters
        ----------
        portfolio: Portfolio
        market_data_service: MarketDataService
        """
        required_market_ids = portfolio_valuation.get_market_ids(portfolio)
        list_of_scenario_numbers = [market_data_service.get_number_scenarios(market_id=market_id) for market_id in required_market_ids]
        number_of_scenarios = min(list_of_scenario_numbers)

        self.__valuation_list = [portfolio_valuation.PortfolioValuation(
            portfolio=portfolio,
            market_data_service=market_data_service,
            scenario_number=scenario_number) for scenario_number in range(number_of_scenarios)]

    def get_all_portfolio_valuations(self):
        return pd.concat([val.get_portfolio_valuation() for val in self.__valuation_list], axis=1)

    def get_all_sharpe_ratios(self, start_date, end_date):
        return [val.get_portfolio_sharpe_ratio(start_date=start_date, end_date=end_date)
                for val in self.__valuation_list]

    def get_all_sharpe_ratios_max_period(self):
        return [val.get_portfolio_sharpe_ratio_max_period() for val in self.__valuation_list]


