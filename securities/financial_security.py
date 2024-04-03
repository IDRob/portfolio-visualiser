import copy


class Security:
    """ Security Class
    An absract class representing a Security
    """

    def __init__(self, *, security_id):
        """
        Initialize the Security Class.

        :param security_id: MarketId
        """
        self.__security_id = copy.deepcopy(security_id)

    def get_security_id(self):
        """
        Gets the security id.

        :return: MarketId
        """
        return copy.deepcopy(self.__security_id)
