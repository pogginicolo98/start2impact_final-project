"""
Functions for managing bids's data stored on Redis.
"""

import json

from redis import Redis
from utils.redis_config import IP_ADDRESS, PORT


def get_latest_bid(auction):
    redis_client = Redis(IP_ADDRESS, port=PORT)
    key = f'Auction n.{auction.pk}'
    try:
        latest_bid_json = redis_client.lrange(key, 0, 0)[0]
    except IndexError:
        raise IndexError
    latest_bid = json.loads(latest_bid_json)
    return latest_bid
