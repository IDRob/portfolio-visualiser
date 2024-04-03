import tkinter as tk
from statistics import mean

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

from valuation.portfolio_valuation import PortfolioValuation
from valuation.scenario_valuation import ScenarioValuation


class PortfolioResults:
    """ Portfolio Results Class
    Shows the financial results for the given market expectations and the given portfolio.
    """
    def __init__(self, frame, market_scenarios, portfolio_builder):
        """
        Initialize the Portfolio Results Class.

        Parameters
        ----------
        frame: the tkinter frame
        market_scenarios: MarketScenarios
        portfolio_builder: PortfolioBuilder
        """
        self.__market_scenarios = market_scenarios
        self.__portfolio_builder = portfolio_builder
        self.__frame = frame
        tk.Button(frame, text='Exit', command=frame.quit).grid(row=1, column=0, sticky=tk.W, pady=4)
        tk.Button(frame, text='Show', command=self._show_results).grid(row=0, column=0, sticky=tk.W, pady=4)

    def _show_results(self):
        market_data_service = self.__market_scenarios.market_data_service
        if market_data_service is not None:
            portfolio_valuation = ScenarioValuation(
                portfolio=self.__portfolio_builder.portfolio,
                market_data_service=market_data_service
            )
            scenario_1_valuation = portfolio_valuation.get_all_portfolio_valuations()
            fig = Figure(figsize=(5, 4), dpi=100)  # create the figure
            ax = fig.add_subplot(111)  # create the subplot
            scenario_1_valuation.plot(ax=ax)

            graph_1 = FigureCanvasTkAgg(fig, master=self.__frame)
            graph_1.get_tk_widget().grid(row=2, column=0)
            graph_1.draw()

            mean_sharpe_ratio = mean(portfolio_valuation.get_all_sharpe_ratios_max_period())
            tk.Label(self.__frame, text='Mean Sharpe Ratio').grid(row=0, column=1)
            tk.Label(self.__frame, text=str(mean_sharpe_ratio)).grid(row=0, column=2)

