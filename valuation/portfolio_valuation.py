import pandas as pd

from marketData.market_data_service import MarketDataService
from marketData.market_id import PriceId, VolatilityId, RiskFreeRateId
from portfolio.portfolio import Portfolio
from positions import financial_position
from positions import common_stock
from positions import option
from pyblackscholesanalytics.market.market import MarketEnvironment
from pyblackscholesanalytics.options.options import PlainVanillaOption


def present_value(*, mkt_env, position_to_value, market_data, scenario_number):
    if isinstance(position_to_value, financial_position.Position):
        security_id = position_to_value.get_security_id()
        quantity = position_to_value.get_quantity()

        price = market_data.get_market_data(market_id=PriceId(security_id=security_id),
                                            scenario_number=scenario_number)
        if isinstance(position_to_value, common_stock.CommonStock):
            return price * quantity
        if isinstance(position_to_value, option.Option):
            strike = position_to_value.strike
            expiry = position_to_value.expiry
            option_type = position_to_value.option_type

            date = market_data.get_date()
            # use the final value of an option if it has expired
            if date > expiry:
                return None
            volatility = market_data.get_market_data(
                market_id=VolatilityId(security_id=security_id),
                scenario_number=scenario_number)

            risk_free_rate = market_data.get_market_data(
                market_id=RiskFreeRateId(security_id=security_id),
                scenario_number=scenario_number)

            mkt_env.set_t(t=date.strftime('%d-%m-%Y'))
            mkt_env.set_r(r=risk_free_rate)
            mkt_env.set_S(S=price)
            mkt_env.set_sigma(sigma=volatility)

            plain_vanilla = PlainVanillaOption(
                mkt_env,
                option_type=option_type,
                K=strike,
                T=expiry.strftime('%d-%m-%Y'))

            price_option = plain_vanilla.get_initial_price()[0]
            return price_option * quantity

    else:
        ValueError("Must be a security to find present value")


def get_market_id(position_to_value):
    if isinstance(position_to_value, financial_position.Position):
        security_id = position_to_value.get_security_id()
        if isinstance(position_to_value, common_stock.CommonStock):
            return [PriceId(security_id=security_id)]
        if isinstance(position_to_value, option.Option):
            return [PriceId(security_id=security_id), VolatilityId(security_id=security_id),
                    RiskFreeRateId(security_id=security_id)]


def get_market_ids(portfolio):
    if isinstance(portfolio, Portfolio):
        positions = portfolio.get_positions()
        market_ids = []
        for position in positions:
            market_ids.extend(get_market_id(position))
        return set(market_ids)


def portfolio_present_value(mkt_env, portfolio, market_data, scenario_number):
    if isinstance(portfolio, Portfolio):
        positions = portfolio.get_positions()
        position_present_values = [present_value(
            mkt_env=mkt_env,
            position_to_value=position,
            market_data=market_data,
            scenario_number=scenario_number) for position in positions]
        return position_present_values


class PortfolioValuation:
    """ Portfolio Valuation Class
    A class that performs valuation on a given portfolio.
    """

    def __init__(self, *, portfolio, market_data_service: MarketDataService, scenario_number):
        """
        Initialize the Portfolio Valuation Class.

        Parameters
        ----------
        portfolio: Portfolio
        market_data_service: MarketDataService
        scenario_number: int
        """
        self.__mkt_env = MarketEnvironment()
        market_data_data_frame = market_data_service.get_date_to_market_data()
        portfolio_value_dict = {}
        for date, row in market_data_data_frame.iterrows():
            market_data = row[0]
            temp_value = portfolio_present_value(
                mkt_env=self.__mkt_env,
                portfolio=portfolio,
                market_data=market_data,
                scenario_number=scenario_number)
            portfolio_value_dict[date] = temp_value

        portfolio_value_df = pd.DataFrame.from_dict(portfolio_value_dict, orient='index')
        portfolio_value_df.fillna(method='pad', inplace=True)

        self.portfolio_securities_valuation = portfolio_value_df

    def get_portfolio_securities_valuation(self):
        return self.portfolio_securities_valuation

    def get_portfolio_valuation(self):
        return pd.DataFrame(self.portfolio_securities_valuation.sum(axis=1), columns=['portfolio'])

    def get_portfolio_pnl(self):
        vals = self.get_portfolio_valuation().loc[:, 'portfolio']
        pnls = vals / vals.shift(1, fill_value=vals[0]) - 1
        return pnls

    def get_portfolio_return(self, *, start_date, end_date):
        vals = self.get_portfolio_valuation()
        start_val = vals.loc[start_date][0]
        end_val = vals.loc[end_date][0]
        return end_val / start_val - 1

    def get_portfolio_volatility(self, *, start_date, end_date):
        pnls = self.get_portfolio_pnl()
        return pnls.std() * pow(255, 0.5)

    def get_portfolio_sharpe_ratio(self, *, start_date, end_date):
        portfolio_return = self.get_portfolio_return(start_date=start_date, end_date=end_date)
        portfolio_vol = self.get_portfolio_volatility(start_date=start_date, end_date=end_date)

        return portfolio_return / portfolio_vol

    def get_portfolio_sharpe_ratio_max_period(self):
        start_date = self.get_portfolio_valuation().index[0]
        end_date = self.get_portfolio_valuation().index[-1]
        portfolio_return = self.get_portfolio_return(start_date=start_date, end_date=end_date)
        portfolio_vol = self.get_portfolio_volatility(start_date=start_date, end_date=end_date)

        return portfolio_return / portfolio_vol
