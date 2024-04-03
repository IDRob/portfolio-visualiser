import tkinter as tk
from tkinter import ttk

from front_end.market_scenarios import MarketScenarios
from front_end.portfolio_builder import PortfolioBuilder
from front_end.portfolio_results import PortfolioResults


class Widget:
    """ Widget Class
    Runs the portfolio valuation visualiser widget.
    """

    def __init__(self):
        """
        Initialize the Widget Class.
        """
        root = tk.Tk()
        root.title("Tab Widget")
        tab_control = ttk.Notebook(root)

        tab1 = ttk.Frame(tab_control)
        tab2 = ttk.Frame(tab_control)
        tab3 = ttk.Frame(tab_control)

        tab_control.add(tab1, text='Market Scenarios')
        tab_control.add(tab2, text='Portfolio Builder')
        tab_control.add(tab3, text='Portfolio Results')
        tab_control.pack(expand=1, fill="both")

        market_securities = MarketScenarios(tab1)
        portfolio_builder = PortfolioBuilder(tab2)

        PortfolioResults(tab3, market_securities, portfolio_builder)

        root.mainloop()
