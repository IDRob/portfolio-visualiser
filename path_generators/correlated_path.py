import random

from path_generators.path import Path
import numpy as np
import pandas as pd

from path_generators.volatile_path import VolatilePath


class CorrelatedPath(Path):
    """
    Takes a central path and produces a number correlated paths each with a given annual volatility.

    The central path must have a non-negligible volatility
    """

    def __init__(self, *, correlation, annual_volatility, number_of_paths, central_path: Path):
        """
        Initialize correlated path

        :param correlation: float
        :param annual_volatility: float
        :param number_of_paths: int
        :param central_path: Path
        """
        central_path_data_frame = central_path.get_path_dataframe()
        central_path_data_frame.rename(columns={0: "Central Path"}, inplace=True)
        self.central_path = Path(path_dataframe=central_path_data_frame)
        central_path_df = self.central_path.get_path_dataframe()
        number_of_returns = len(central_path_df)
        linalg = np.linalg
        daily_volatility = annual_volatility / pow(255, 0.5)

        corr = []
        for i in range(number_of_paths + 1):
            corr_row = [correlation] * number_of_paths
            corr_row.insert(i, 1)
            corr.append(corr_row)

        total_data_frame = pd.DataFrame(index=central_path_df.index)
        for index in range(central_path_df.shape[1]):

            title = [*central_path_df][index]
            mean = central_path_df.mean()[title]
            std = central_path_df.std()[title]

            correlated_path_dict = {}
            if std < 0.00000000001:
                correlated_path_dict = VolatilePath(
                    volatility=annual_volatility,
                    number_of_paths=1,
                    central_path=central_path).get_path_dataframe()
            else:
                normalised = [((central_path_df[title].to_numpy() - mean) / std)]
                L = linalg.cholesky(corr)
                uncorrelated = np.random.standard_normal((number_of_paths, number_of_returns))
                total = np.concatenate((normalised, uncorrelated), axis=0)
                correlated = np.dot(L, total).transpose()
                correlated_minus_central = correlated[:, 1:]

                for i in range(central_path_df.shape[0]):
                    date = central_path_df.index[i]
                    selected = correlated_minus_central[i]
                    correlated_path_dict[date] = selected * daily_volatility + mean

            data_frame = pd.DataFrame.from_dict(correlated_path_dict, orient='index')
            total_data_frame = pd.concat([total_data_frame, data_frame], axis=1)

        super().__init__(path_dataframe=total_data_frame)

    def get_correlations(self):
        joined = pd.concat([self.central_path.get_path_dataframe(), self.get_path_dataframe()], axis=1)
        return joined.corr().iloc[0, 0:]

