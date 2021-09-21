from random import randrange
from django.utils.timezone import timedelta


def random_date(start, end):
    """
    This function will return a random datetime between two datetime
    objects.
    """

    delta = end - start
    int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
    random_second = randrange(int_delta)
    return start + timedelta(seconds=random_second)
