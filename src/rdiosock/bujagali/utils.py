import random

_random = random.Random()


def randomID(upper=10000000, lower=0):
    return _random.randint(lower, upper)
