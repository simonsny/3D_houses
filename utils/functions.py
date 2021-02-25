def find_index(coord: float, index: str) -> str:
    """
    Function that finds the index in which the coordinates lies
    :param coord: Coordinate
    :param index: index of pd.DataFrame, each index is made up of two coordinates in a tuple, as a string
    :return: Index
    """
    for i in index:
        list_i = [int(s) for s in i.strip('()').split(', ')]
        if (coord > float(list_i[0])) & (coord <= float(list_i[1])):
            return i