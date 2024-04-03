import copy
from datetime import datetime, timedelta
import pandas as pd


class Path:
    """ Path Class
    Holds dictionary of datetime to value for financial instrument.
    """

    DAYS_IN_YEAR = 255

    def __init__(self, *, path_dataframe=None, path_cumulative_data_frame=None):
        """
        Initialise Path Class.

        :param path_dataframe: dataframe of datetime to paths
        """
        if path_cumulative_data_frame is not None:
            self.__path_dataframe = copy.deepcopy(path_cumulative_data_frame.pct_change().fillna(0))
        else:
            self.__path_dataframe = copy.deepcopy(path_dataframe)

    def get_path_dataframe(self):
        """
        Gets dataframe from datetime to value for the paths.

        :return: dataframe of datetime to paths
        """
        return copy.deepcopy(self.__path_dataframe)

    def get_cumulative_path(self, *, start_value):
        """
        Gets the cumulative path dataframe starting from a given value.

        Parameters
        ----------
        start_value: float

        Returns DataFrame
        -------
        """
        dataframe = self.__path_dataframe

        __running__value = [start_value] * len(dataframe.columns)
        cumulative_path_dict = {dataframe.index[0]: __running__value}
        for index, row in dataframe.iloc[1:].iterrows():
            daily_return = row
            __running__value = [r * (1 + d) for r, d in zip(__running__value, daily_return)]
            today_value = copy.deepcopy(__running__value)
            cumulative_path_dict[index] = today_value

        data_frame = pd.DataFrame.from_dict(cumulative_path_dict, orient='index', columns=dataframe.columns.values)
        return data_frame

    def repeat_scenarios(self, multiplier):
        """
        Takes the existing scenarios in the dataframe and repeats them by the multiplier number return a new Path
        object.

        E.g. if there is a single scenario and a multiple of 10 is given. A Path object with a dataframe with 10
        identical scenarios will be returned
        Parameters
        ----------
        multiplier: int

        Returns Path
        -------
        """
        return Path(path_dataframe=pd.concat([self.__path_dataframe] * multiplier, axis=1, ignore_index=True))


def get_previous_working_day(day):
    """
    Gets the most recent working day previous to the given day.

    Parameters
    ----------
    day: datetime

    Returns datetime
    -------

    """
    delta = timedelta(days=1)
    d = day
    d -= delta
    weekend = {5, 6}
    while d in weekend:
        d -= delta
    return d


def get_next_working_day(day):
    """
    Get the mot soon working day, next after the given day.
    Parameters
    ----------
    day: datetime

    Returns datetime
    -------
    """
    delta = timedelta(days=1)
    d = day
    d += delta
    weekend = {5, 6}
    while d in weekend:
        d += delta
    return d
