import tkinter as tk
import datetime

from portfolio.portfolio import Portfolio
from positions import common_stock, option


class PortfolioBuilder:
    """ Portfolio Builder Class
    Allows user to build a portfolio of positions.
    """

    def __init__(self, frame):
        """
        Initialize the Portfolio Builder Class.

        Parameters
        ----------
        frame: the tkinter frame
        """

        # self.portfolio is public so that it can be accessed by Portfolio Results.
        self.portfolio = Portfolio()

        inputs_frame = tk.Frame(frame)
        self._show_portfolio_screen = tk.Frame(frame)

        inputs_frame.grid(row=0, column=0)
        self._show_portfolio_screen.grid(row=0, column=2)

        tk.Label(inputs_frame, text='Number').grid(row=0)

        tk.Label(inputs_frame, text='Type').grid(row=1)
        tk.Label(inputs_frame, text='Strike').grid(row=2)

        self.__quantity = tk.Entry(inputs_frame,
                                   textvariable=tk.StringVar(inputs_frame, value='1'))
        self.__type_of_position = tk.StringVar(inputs_frame)
        self.__type_of_position.set('common stock')
        tk.OptionMenu(
            inputs_frame,
            self.__type_of_position,
            'common stock', "call", "put").grid(row=1, column=1)

        self.__strike = tk.Entry(inputs_frame,
                                 textvariable=tk.StringVar(inputs_frame, value='100'))

        self.__quantity.grid(row=0, column=1)
        self.__strike.grid(row=2, column=1)

        tk.Button(inputs_frame, text='Exit', command=frame.quit).grid(row=6, column=0, sticky=tk.W, pady=4)
        tk.Button(inputs_frame, text='Add Item', command=self._add_position).grid(row=7, column=0, sticky=tk.W, pady=4)
        tk.Button(inputs_frame, text='Delete Portfolio', command=self._delete_portfolio).grid(row=8, column=0,
                                                                                              sticky=tk.W, pady=4)

    def _add_position(self):
        type_of_position = str(self.__type_of_position.get())
        number = float(self.__quantity.get())
        strike = float(self.__strike.get())

        if type_of_position == "common stock":
            self.portfolio.add_position(position=common_stock.CommonStock(security_id=1, quantity=number))
            tk.Label(self._show_portfolio_screen, text=str(number) + type_of_position).pack()
        else:
            self.portfolio.add_position(position=option.Option(
                security_id=1,
                quantity=number,
                expiry=datetime.datetime(2025, 1, 15, 0, 0),
                strike=strike,
                option_type=type_of_position))
            tk.Label(self._show_portfolio_screen,
                     text=str(number) + type_of_position + ", strike=" + str(strike)).pack()

    def _delete_portfolio(self):
        for widget in self._show_portfolio_screen.winfo_children():
            widget.destroy()
        self.portfolio = Portfolio()
