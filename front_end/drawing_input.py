import datetime
import tkinter as tk
import pandas as pd
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from matplotlib.figure import Figure

from path_generators.linear_path import LinearPath


class DrawingInput:
    """ Drawing Input Class
    Canvas and tools for user to draw the shape of a market expectation.
    """

    def __init__(self, frame):
        """
        Initialize Drawing Input class.

        Parameters
        ----------
        frame: the tkinter frame which holds the drawing input canvas
        """
        self.line_id = None
        self.line_points = []
        self.line_options = {}
        self.canvas = (tk.Canvas(frame))
        self.canvas.grid(row=1, column=3)
        self.canvas.bind('<Button-1>', self._set_start)
        self.canvas.bind('<B1-Motion>', self._draw_line)
        self.canvas.bind('<ButtonRelease-1>', self._end_line)
        tk.Button(frame, text='Clear Draw', command=self._clear_line).grid(row=2, column=3, sticky=tk.W, pady=4)

    def _draw_line(self, event):
        self.line_points.extend((event.x, event.y))
        if self.line_id is not None:
            self.canvas.delete(self.line_id)
        self.line_id = self.canvas.create_line(self.line_points, **self.line_options)

    def _set_start(self, event):
        self.line_points.extend((event.x, event.y))

    def _end_line(self, event=None):
        var = self.line_id

    def _clear_line(self):
        self.canvas.delete(self.line_id)
        self.line_points = []
        self.line_id = None
        self.line_options = {}

    def plot_drawn_graph(self, *, target_start, target_peak, target_trough, start_date, end_date):
        linear_path = LinearPath(daily_value=0.0, start_date=start_date, end_date=end_date)
        values = self.line_points

        x_axis = values[::2]
        y_axis_orig = values[1::2]
        starting = [281] * len(y_axis_orig)
        y_axis = []
        for x in range(len(y_axis_orig)):
            y_axis.append(starting[x] - y_axis_orig[x])
        cum_values = pd.DataFrame(y_axis, index=x_axis)
        cum_values = cum_values[~cum_values.index.duplicated(keep='first')]

        r = pd.RangeIndex(0, linear_path.get_path_dataframe().shape[0] + 1, 1)
        t = cum_values
        t = t.sort_index()
        new_idx = np.linspace(t.index[0], t.index[-1], len(r))
        new_cum = t.reindex(new_idx, method='ffill', limit=1).iloc[1:].interpolate()

        complete = pd.DataFrame(new_cum.values, index=linear_path.get_path_dataframe().index.copy())
        current_peak = complete.max()[0]
        current_trough = complete.min()[0]

        current_start = complete.iloc[0][0]

        return self._stretch_and_translate_path(complete, target_start, current_start, current_peak, target_peak,
                                                current_trough, target_trough)

    def _get_multiplier(self, start_target, current_start, current_peak, current_target):
        if current_start != current_peak:
            return (current_target - start_target) / (current_peak - current_start)
        else:
            return 0

    def _stretch_and_translate_path(self, path, start_target, current_start, current_peak, target_peak,
                                    current_trough, target_trough):

        max_multiplier = self._get_multiplier(start_target, current_start, current_peak, target_peak)
        max_addition = start_target - current_start * max_multiplier

        min_multiplier = self._get_multiplier(start_target, current_start, current_trough, target_trough)
        min_addition = start_target - current_start * min_multiplier

        max_path = path.where(path >= current_start).mul(max_multiplier).add(max_addition).fillna(0)
        min_path = path.where(path < current_start).mul(min_multiplier).add(min_addition).fillna(0)
        return sum([max_path, min_path])
