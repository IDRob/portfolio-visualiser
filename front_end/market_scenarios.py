import tkinter as tk
import pandas as pd
import datetime

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

from front_end.drawing_input import DrawingInput
from marketData.market_data_service import MarketDataService
from marketData.market_id import PriceId, VolatilityId, RiskFreeRateId
from path_generators.correlated_path import CorrelatedPath
from path_generators.linear_path import LinearPath
from path_generators.path import Path
from path_generators.volatile_path import VolatilePath


class MarketScenarios:
    """ Market Scenarios Class
    Allows the user to build their market expectation scenarios.
    """
    def __init__(self, frame):
        """
        Initialize the Market Scenario Class.

        Parameters
        ----------
        frame: tkinter frame
        """

        self.market_data_service = None
        drawing_input_frame = tk.Frame(frame)
        numerical_inputs_frame = tk.Frame(frame)
        self.__graph_frame = tk.Frame(frame)
        self.__drawing_input = DrawingInput(drawing_input_frame)

        numerical_inputs_frame.grid(row=0, column=0)
        drawing_input_frame.grid(row=0, column=1)
        self.__graph_frame.grid(row=0, column=2)

        tk.Label(numerical_inputs_frame, text='Starting Point').grid(row=0)
        tk.Label(numerical_inputs_frame, text='Max Height').grid(row=1)
        tk.Label(numerical_inputs_frame, text='Min Height').grid(row=2)
        tk.Label(numerical_inputs_frame, text='Target Vol').grid(row=3)
        tk.Label(numerical_inputs_frame, text='Number of scenarios').grid(row=4)

        self.__starting_point = tk.Entry(numerical_inputs_frame,
                                         textvariable=tk.StringVar(numerical_inputs_frame, value='100'))
        self.__maximum_height = tk.Entry(numerical_inputs_frame,
                                         textvariable=tk.StringVar(numerical_inputs_frame, value='120'))
        self.__min_height = tk.Entry(numerical_inputs_frame,
                                     textvariable=tk.StringVar(numerical_inputs_frame, value='90'))
        self.__target_vol = tk.Entry(numerical_inputs_frame,
                                     textvariable=tk.StringVar(numerical_inputs_frame, value='0.2'))
        self.__number_of_scenarios = tk.Entry(numerical_inputs_frame, textvariable=tk.StringVar(frame, value='10'))

        self.__starting_point.grid(row=0, column=1)
        self.__maximum_height.grid(row=1, column=1)
        self.__min_height.grid(row=2, column=1)
        self.__target_vol.grid(row=3, column=1)
        self.__number_of_scenarios.grid(row=4, column=1)

        tk.Button(numerical_inputs_frame, text='Exit', command=frame.quit).grid(row=6, column=0, sticky=tk.W, pady=4)
        tk.Button(numerical_inputs_frame, text='Create Graph', command=self._show_data).grid(row=7, column=0,
                                                                                             sticky=tk.W, pady=4)

    def _show_data(self):
        __starting_point = float(self.__starting_point.get())
        __max_height = float(self.__maximum_height.get())
        __min_height = float(self.__min_height.get())
        __volatility = float(self.__target_vol.get())
        __number_of_scenarios = int(self.__number_of_scenarios.get())

        __start_date = datetime.datetime(2023, 12, 15, 0, 0)
        __end_date = datetime.datetime(2024, 12, 15, 0, 0)

        path = self.__drawing_input.plot_drawn_graph(
            target_start=__starting_point,
            target_peak=__max_height,
            target_trough=__min_height,
            start_date=__start_date,
            end_date=__end_date)

        central_path = Path(path_cumulative_data_frame=path)
        path_to_correlate_with = (
            VolatilePath(volatility=__volatility, number_of_paths=__number_of_scenarios, central_path=central_path))

        cum_values = pd.concat([central_path.get_cumulative_path(
            start_value=__starting_point),
            path_to_correlate_with.get_cumulative_path(start_value=__starting_point)], axis=1)

        fig = Figure(figsize=(5, 4), dpi=100)  # create the figure
        ax = fig.add_subplot(111)  # create the subplot
        cum_values.plot(ax=ax)

        graph_1 = FigureCanvasTkAgg(fig, master=self.__graph_frame)
        graph_1.get_tk_widget().grid(row=1, column=4)
        graph_1.draw()

        if not path_to_correlate_with.get_path_dataframe().empty:
            # Market Data service is public so that it can be accessed by portfolio results.
            self.market_data_service = MarketDataService()
            self.market_data_service.add_market_data_from_path(
                path_data_frame=path_to_correlate_with.get_cumulative_path(start_value=100),
                market_id=PriceId(security_id=1))

            implied_vol_path = (LinearPath(daily_value=__volatility, start_date=__start_date, end_date=__end_date)
                                .repeat_scenarios(__number_of_scenarios))

            self.market_data_service.add_market_data_from_path(
                path_data_frame=implied_vol_path.get_path_dataframe(),
                market_id=VolatilityId(security_id=1))

            risk_free_path = (LinearPath(daily_value=0.04, start_date=__start_date, end_date=__end_date)
                              .repeat_scenarios(__number_of_scenarios))

            self.market_data_service.add_market_data_from_path(
                path_data_frame=risk_free_path.get_path_dataframe(),
                market_id=RiskFreeRateId(security_id=1))
