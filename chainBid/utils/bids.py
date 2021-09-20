"""
Common functions for managing bids.
"""

import json

from redis import Redis
from utils.redis_config import IP_ADDRESS, PORT


def get_user_latest_bid(auction):
    redis_client = Redis(IP_ADDRESS, port=PORT)
    key = f'Auction n.{auction.pk}'
    try:
        last_bid_json = redis_client.lrange(key, 0, 0)[0]
    except IndexError:
        return ''
    last_bid = json.loads(last_bid_json)
    return last_bid.get('user')


def get_price_latest_bid_or_initial_price(auction):
    redis_client = Redis(IP_ADDRESS, port=PORT)
    key = f'Auction n.{auction.pk}'
    try:
        last_bid_json = redis_client.lrange(key, 0, 0)[0]
    except IndexError:
        return auction.initial_price
    last_bid = json.loads(last_bid_json)
    return last_bid.get('price')
