from datetime import datetime, timedelta

from path_generators.path import Path, get_next_working_day
import pandas as pd


class LinearPath(Path):
    """ Linear Path Class
    A path which has a uniform daily return from start date to end date.
    """

    def __init__(self, *, daily_value, start_date, end_date):
        """
        Initialize a linear path.

        :param daily_value: float
        :param start_date: datetime
        :param end_date: datetime
        """

        path = {}
        delta = timedelta(days=1)
        d = start_date - delta
        while d <= end_date:
            d = get_next_working_day(d)
            path[d] = daily_value
        path = pd.DataFrame.from_dict(path, orient='index')
        super().__init__(path_dataframe=path)

