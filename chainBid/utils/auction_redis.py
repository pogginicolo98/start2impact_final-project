import json

from django.conf import settings
from redis import Redis
from utils.encoders_decoders import AuctionDecoder, AuctionEncoder

TASKS_KEY = 'tasks'
BIDS_KEY = 'bids'


def record_object_on_redis(auction, **kwargs):
    """
    Record an object on Redis.

    :kwargs
    1) Auction tasks: 'task_id'.
    3) Bid: 'user', 'price', 'eta' (optional).
    """

    key = None
    obj = None
    if kwargs.get('task_id', None) is not None:
        key = f'auction_{auction}_{TASKS_KEY}'
        obj = {
            'task_id': kwargs['task_id']
        }
    elif kwargs.get('price', None) is not None:
        key = f'auction_{auction}_{BIDS_KEY}'
        obj = {
            'user': kwargs.get('user', None),
            'price': kwargs['price'],
            'eta': kwargs.get('eta', None)
        }
    if key is not None and obj is not None:
        redis_client = Redis(settings.REDIS_HOST, port=settings.REDIS_PORT)
        value = json.dumps(obj, cls=AuctionEncoder)
        redis_client.lpush(key, value)


def get_latest_object_on_redis(auction, type_obj):
    """
    Get the latest object recorded on Redis.

    :type_obj
    1) TASKS_KEY: Return the latest schedule/close auction task.
    2) BIDS_KEY: Return the latest bid.

    :return
    - None: If no bid is found.
    - obj: Dictionary.
    """

    redis_client = Redis(settings.REDIS_HOST, port=settings.REDIS_PORT)
    key = f'auction_{auction}_{type_obj}'
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
    key = f'auction_{auction}_{BIDS_KEY}'
    value = redis_client.exists(key)
    if value:
        return True
    return False


def clean_db(auction):
    """
    Delete bids and related data from Redis db.
    """

    redis_client = Redis(settings.REDIS_HOST, port=settings.REDIS_PORT)
    key1 = f'auction_{auction}_{TASKS_KEY}'
    key2 = f'auction_{auction}_{BIDS_KEY}'
    key3 = f'asgi:group:auction_{auction}'
    redis_client.delete(key1, key2, key3)
