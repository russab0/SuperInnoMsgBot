class CountDict(dict):
    """
    Class that is used as counter, inherited from dict.
    """

    def __getitem__(self, item):
        """
        Gets item without exceptions
        :param item:  key you want to get
        :return: value, associated with `item` (if item in the `keys`), 0 otherwise
        """
        if item not in self:
            return 0
        return super().__getitem__(item)