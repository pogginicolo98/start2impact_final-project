from django.utils.timezone import timedelta
from random import choice, randrange
from string import ascii_lowercase, digits

ALPHANUMERIC_CHARS = ascii_lowercase + digits
STRING_LENGTH = 6


def random_date(start, end):
    """
    Return a random datetime between two datetime objects.
    """

    delta = end - start
    int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
    random_second = randrange(int_delta)
    return start + timedelta(seconds=random_second)


def generate_random_string(chars=ALPHANUMERIC_CHARS, length=STRING_LENGTH):
    """
    Generate a random string starting from a set of chars and of fixed length.
    """

    return "".join(choice(chars) for _ in range(length))
