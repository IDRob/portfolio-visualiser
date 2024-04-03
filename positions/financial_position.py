import copy


class Position:
    """ Position Class
    An absract class representing a Financial Position.
    """

    def __init__(self, *, security, quantity):
        self.__security = copy.deepcopy(security)
        self.__quantity = copy.deepcopy(quantity)

    def get_security_id(self):
        return self.__security.get_security_id()

    def get_quantity(self):
        return copy.deepcopy(self.__quantity)

    def get_type(self):
        return 0
