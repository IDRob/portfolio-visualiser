import unittest

from portfolio import Portfolio
from positions import common_stock
from positions import option
import datetime


class TestPortfolio(unittest.TestCase):
    # Test Class for Portfolio Class
    __portfolio = Portfolio()

    def test_add_position(self):
        self.__portfolio.add_position(position=common_stock.CommonStock(security_id=1, quantity=100))

        self.__portfolio.add_position(position=option.Option(
            security_id=1,
            quantity=1,
            expiry=datetime.datetime(2024, 1, 15, 0, 0),
            strike=1.2,
            option_type="call"))
        portfolio = self.__portfolio.get_positions()


        self.assertEqual(len(portfolio), 2)
