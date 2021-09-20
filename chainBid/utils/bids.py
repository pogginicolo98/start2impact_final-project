"""
Functions for managing bids's data stored on Redis.
"""

import json

from redis import Redis
from utils.redis_config import IP_ADDRESS, PORT


def get_latest_bid(auction):
    """
    Read from Redis the last auction's bid placed.

    :param
    - auction: Auction instance.

    :return
    - {'user', 'admin', 'price': 9.99}.

    * IndexError handling is required.
    """

    redis_client = Redis(IP_ADDRESS, port=PORT)
    key = f'Auction n.{auction.pk}'
    try:
        latest_bid_json = redis_client.lrange(key, 0, 0)[0]
    except IndexError:
        raise IndexError
    latest_bid = json.loads(latest_bid_json)
    return latest_bid


def place_new_bid(auction, user, price):
    """
    Record on Redis a new auction's bid.

    :param
    - auction: Auction instance.
    - user
    - price
    """

    redis_client = Redis(IP_ADDRESS, port=PORT)
    key = f'Auction n.{auction.pk}'
    bid = {
        'user': user,
        'price': price
    }
    value = json.dumps(bid)
    redis_client.lpush(key, value)
