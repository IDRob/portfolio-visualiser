import copy

from positions import financial_position


class Portfolio:
    """ Portfolio Class
    Holds positions in the portfolio.
    """

    def __init__(self):
        self.__positions = []

    def add_position(self, *, position: financial_position.Position):
        """
        Adds position to the portfolio.

        :param position: Position
        :return: none
        """
        self.__positions.append(copy.deepcopy(position))

    def get_positions(self):
        """
        Gets positions in the portfolio.

        :return: List of Positions
        """
        return copy.deepcopy(self.__positions)
