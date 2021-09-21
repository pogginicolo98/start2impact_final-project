from auctions.models import Auction
from chainBid.celery import app
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.shortcuts import get_object_or_404
from utils.bids import get_latest_bid
from utils.randomics import random_date

UserModel = get_user_model()


@app.task
def close_auction(pk):
    """
    ???
    """

    auction = get_object_or_404(Auction, pk=pk)
    try:
        latest_bid = get_latest_bid(auction)
        user = get_object_or_404(UserModel, username=latest_bid['user'])
        auction.won_by = user
        auction.final_price = latest_bid['price']
    except IndexError:
        pass
    auction.status = not auction.status
    auction.closed_at = timezone.now()
    auction.save()


def update_remaining_time_bid(auction, *task_id):
    """
    Record on Redis a new auction's bid.

    :param
    - auction: Auction instance.
    - user
    - price

    permanent revoke:
    celery worker -A proj --statedb=/var/run/celery/worker.state
    initialize celery worker when executing the celery start command.
    """

    redis_client = Redis(IP_ADDRESS, port=PORT)
    key = f'Auction n.{auction.pk} - remaining time'
    if task_id:
        value = task_id
    else:
        value = redis_client.lpop(key)
        old_task_id = json.loads(value)
        app.control.revoke(old_task_id, terminate=True)
        value = close_auction.apply_async((auction.pk,), countdown=15)
    redis_client.lpush(key, value)


@app.task
def open_auction(pk):
    """
    Auction asynchronous task.
    When the opening_date occurs, the auction toggle its status to enabled.
    """

    auction = get_object_or_404(Auction, pk=pk)
    auction.status = not auction.status
    auction.save()

    min_duration = auction.opening_date + timezone.timedelta(hours=20)
    max_duration = auction.opening_date + timezone.timedelta(hours=24)
    closing_date = random_date(start=min_duration, end=max_duration)
    task_id = close_auction.apply_async((pk,), eta=closing_date)
    update_remaining_time_bid(auction, task_id)
