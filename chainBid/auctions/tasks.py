from auctions.models import Auction, AuctionReport
from chainBid.celery import app
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from utils.auction_redis import get_latest_object_on_redis, record_object_on_redis, TASKS_KEY


UserModel = get_user_model()


@app.task
def close_auction(pk):
    """
    Auction asynchronous task.
    Executed when the maximum closing date occurs or a user wins.
    """

    auction = get_object_or_404(Auction, pk=pk)
    auction.close()
    AuctionReport.objects.create(auction=auction)


@app.task
def open_auction(pk, max_closing_date):
    """
    Auction asynchronous task.
    Executed when the opening date occurs.
    """

    auction = get_object_or_404(Auction, pk=pk)
    auction.open()
    close_auction_task = close_auction.apply_async((pk,), eta=max_closing_date).id
    record_object_on_redis(auction=auction.pk, task_id=close_auction_task)


def update_close_auction(pk, eta):
    """
    When a new bid is placed, the last celery task that is handling the closing of the auction is revoked and
    a new one is created with 15 seconds of countdown.
    """

    previous_task = get_latest_object_on_redis(auction=pk, type_obj=TASKS_KEY)
    if previous_task is not None:
        if previous_task.get('task_id', None):
            app.control.revoke(previous_task['task_id'], terminate=True, signal='SIGKILL')
    close_auction_task = close_auction.apply_async((pk,), eta=eta).id
    record_object_on_redis(auction=pk, task_id=close_auction_task)
