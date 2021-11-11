import math


def get_euclid_distance(point1: tuple, point2: tuple) -> float:
    return math.sqrt(math.pow((point1[0] - point2[0]), 2) + math.pow((point1[1] - point2[1]), 2))
