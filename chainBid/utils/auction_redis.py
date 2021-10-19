import json
from django.conf import settings
from redis import Redis
from utils.encoders_decoders import AuctionDecoder, AuctionEncoder

SCHEDULE_KEY = 'schedule'
BIDS_KEY = 'bids'
CLOSE_KEY = 'close'


def record_object_on_redis(auction, **kwargs):
    """
    Record an object on Redis.

    :kwargs
    1) Schedule auction task: 'schedule_id'.
    2) Close auction task: 'close_id', 'eta' (optional).
    3) Bid: 'bid_user', 'bid_price'.
    """

    key = None
    obj = None
    if kwargs.get('schedule_id', None) is not None:
        key = f'Auction n.{auction} - {SCHEDULE_KEY}'
        obj = {'task_id': kwargs['schedule_id']}
    elif kwargs.get('close_id', None) is not None:
        key = f'Auction n.{auction} - {CLOSE_KEY}'
        obj = {
            'task_id': kwargs['close_id'],
            'eta': kwargs.get('eta', None)
        }
    elif kwargs.get('bid_user', None) is not None and kwargs.get('bid_price', None) is not None:
        key = f'Auction n.{auction} - {BIDS_KEY}'
        obj = {
            'user': kwargs['bid_user'],
            'price': kwargs['bid_price']
        }
    if key is not None and obj is not None:
        redis_client = Redis(settings.REDIS_HOST, port=settings.REDIS_PORT)
        value = json.dumps(obj, cls=AuctionEncoder)
        redis_client.lpush(key, value)


def get_latest_object_on_redis(auction, type_obj):
    """
    Get the latest object recorded on Redis.

    :type_obj
    1) 'schedule': Return the latest schedule auction task.
    2) 'close': Return the latest close auction task.
    3) 'bids': Return the latest bid.

    :return
    - None: If no bid is found.
    - obj: Dictionary.
    """

    redis_client = Redis(settings.REDIS_HOST, port=settings.REDIS_PORT)
    key = f'Auction n.{auction} - {type_obj}'
    value = redis_client.lrange(key, 0, 0)
    if value is not None and len(value) > 0:
        return json.loads(value[0], cls=AuctionDecoder)
    return None


def auction_started(auction):
    """
    Check if the auction is started.

    :return
    - True: If started.
    - False: If not started.
    """

    redis_client = Redis(settings.REDIS_HOST, port=settings.REDIS_PORT)
    key = f'Auction n.{auction} - {BIDS_KEY}'
    value = redis_client.exists(key)
    if value:
        return True
    return False


def clean_db(auction):
    """
    Delete bids and related data from Redis db.
    """

    redis_client = Redis(settings.REDIS_HOST, port=settings.REDIS_PORT)
    key1 = f'Auction n.{auction} - {SCHEDULE_KEY}'
    key2 = f'Auction n.{auction} - {BIDS_KEY}'
    key3 = f'Auction n.{auction} - {CLOSE_KEY}'
    redis_client.delete(key1, key2, key3)
