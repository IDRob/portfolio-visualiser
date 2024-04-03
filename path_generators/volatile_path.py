import random

from path_generators.path import Path
import pandas as pd
import numpy as np


class VolatilePath(Path):
    """ Volatile Path Class
    Produces a volatile path from a given central path.
    """

    def __init__(self, *, volatility, number_of_paths, central_path):
        """
        Initialize the Volatile Path Class

        Parameters
        ----------
        volatility: float
        number_of_paths: int
        central_path: Path
        """
        if isinstance(central_path, Path):
            central_path_data_frame = central_path.get_path_dataframe()
            central_path_data_frame.rename(columns={0: "Central Path"}, inplace=True)
            self.central_path = Path(path_dataframe=central_path_data_frame)
            central_path_df = self.central_path.get_path_dataframe()
            number_of_returns = len(central_path_df)

            daily_volatility = volatility / pow(self.DAYS_IN_YEAR, 0.5)
            uncorrelated = np.random.standard_normal((number_of_paths, number_of_returns)).transpose()

            correlated_path_dict = {}
            for i in range(central_path_df.shape[0]):
                date = central_path_df.index[i]
                selected = uncorrelated[i]
                drift = central_path_df.loc[date, "Central Path"]
                correlated_path_dict[date] = [s * daily_volatility + drift for s in selected]

            path = pd.DataFrame.from_dict(correlated_path_dict, orient='index')
            super().__init__(path_dataframe=path)
        else:
            raise ValueError("Path is wrong object")
