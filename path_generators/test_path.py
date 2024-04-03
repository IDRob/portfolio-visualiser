import datetime
import unittest
import pandas as pd
import numpy as np

from path_generators.correlated_path import CorrelatedPath
from path_generators.linear_path import LinearPath
from path_generators.path import Path
from path_generators.volatile_path import VolatilePath


class TestPath(unittest.TestCase):
    np.random.seed(1000)
    __start_date = datetime.datetime(2023, 12, 15, 0, 0)
    __end_date = datetime.datetime(2024, 12, 15, 0, 0)

    def test_linear_path(self):
        annual_drift = 0.4
        daily_drift = pow(1 + annual_drift, 1 / 255) - 1
        path = LinearPath(daily_value=daily_drift, start_date=self.__start_date,
                          end_date=self.__end_date).get_path_dataframe()

        mean = pow(1 + path.mean().mean(), 255) - 1
        self.assertAlmostEqual(mean, annual_drift, 10)

    def test_path_cum(self):
        annual_drift = 0.4
        daily_drift = pow(1 + annual_drift, 1 / 255) - 1
        start_value = 100
        original_cum_path = LinearPath(
            daily_value=daily_drift,
            start_date=self.__start_date,
            end_date=self.__end_date).get_cumulative_path(start_value=start_value)
        remade_cum_path = Path(
            path_cumulative_data_frame=original_cum_path).get_cumulative_path(start_value=start_value)

        pd.testing.assert_frame_equal(original_cum_path, remade_cum_path)

    def test_volatile_path(self):
        volatility = 0.5
        annual_drift = 0.4
        daily_drift = pow(1 + annual_drift, 1 / 255) - 1
        linear_path = LinearPath(daily_value=daily_drift, start_date=self.__start_date, end_date=self.__end_date)
        volatile_path = VolatilePath(volatility=volatility, number_of_paths=10000, central_path=linear_path)
        path_data_frame = volatile_path.get_path_dataframe()
        std = path_data_frame.std().mean() * pow(255, 0.5)
        mean = pow(1 + path_data_frame.mean().mean(), 255) - 1

        self.assertAlmostEqual(std, volatility, 2)
        self.assertAlmostEqual(mean, annual_drift, 2)

    def test_correlated_path(self):
        volatility = 0.1
        annual_drift = 0.20
        daily_drift = pow(1 + annual_drift, 1 / 255) - 1
        correlated_vols = 0.1
        correlation = 0.8
        linear_path = LinearPath(daily_value=daily_drift, start_date=self.__start_date, end_date=self.__end_date)
        path_to_correlate_with = VolatilePath(volatility=volatility, number_of_paths=1, central_path=linear_path)

        correlated_path = CorrelatedPath(
            correlation=correlation,
            annual_volatility=correlated_vols,
            number_of_paths=2000,
            central_path=path_to_correlate_with)

        correlations = correlated_path.get_correlations()
        correlation_mean = correlations.mean()
        std_mean = correlated_path.get_path_dataframe().std().mean() * pow(255, 0.5)

        self.assertAlmostEqual(correlation_mean, correlation, 2)
        self.assertAlmostEqual(std_mean, correlated_vols, 2)

    def test_multi_volatile_to_correlated_path(self):
        volatility = 0.4
        annual_drift = 0.20
        daily_drift = pow(1 + annual_drift, 1 / 255) - 1
        correlated_vols = 0.05
        correlation = 0.5
        linear_path = LinearPath(daily_value=daily_drift, start_date=self.__start_date, end_date=self.__end_date)
        path_to_correlate_with = VolatilePath(volatility=volatility, number_of_paths=2, central_path=linear_path)

        correlated_path = CorrelatedPath(
            correlation=correlation,
            annual_volatility=correlated_vols,
            number_of_paths=2,
            central_path=path_to_correlate_with)
        correlated_path_data_frame = correlated_path.get_path_dataframe()

        std_mean = correlated_path_data_frame.std().mean() * pow(255, 0.5)

        self.assertAlmostEqual(std_mean, correlated_vols, 2)
