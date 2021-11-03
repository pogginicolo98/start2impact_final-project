from asgiref.sync import async_to_sync
from auctions.models import Auction, AuctionReport
from chainBid.celery import app
from channels.layers import get_channel_layer
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from utils.auction_redis import clean_db, get_latest_object_on_redis, record_object_on_redis, TASKS_KEY


UserModel = get_user_model()


@app.task
def close_auction(slug):
    """
    Auction asynchronous task.
    Executed when the maximum closing date occurs or a user wins.
    """

    auction = get_object_or_404(Auction, slug=slug)
    auction.close()
    channel_layer = get_channel_layer()
    channel_group = slug
    async_to_sync(channel_layer.group_send)(
        channel_group,
        {
            'type': 'auction_closed',
            'winner': auction.winner.username if auction.winner else None
        }
    )
    clean_db(auction=slug)
    AuctionReport.objects.create(auction=auction)


@app.task
def open_auction(slug, max_closing_date):
    """
    Auction asynchronous task.
    Executed when the opening date occurs.
    """

    auction = get_object_or_404(Auction, slug=slug)
    auction.open()
    close_auction_task = close_auction.apply_async((slug,), eta=max_closing_date).id
    record_object_on_redis(auction=auction.slug, task_id=close_auction_task)


def update_close_auction(slug, eta):
    """
    When a new bid is placed, the last celery task that is handling the closing of the auction is revoked and
    a new one is created with 15 seconds of countdown.
    """

    previous_task = get_latest_object_on_redis(auction=slug, type_obj=TASKS_KEY)
    if previous_task is not None:
        if previous_task.get('task_id', None):
            app.control.revoke(previous_task['task_id'], terminate=True, signal='SIGKILL')
    close_auction_task = close_auction.apply_async((slug,), eta=eta).id
    record_object_on_redis(auction=slug, task_id=close_auction_task)
