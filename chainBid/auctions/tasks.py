from auctions.models import Auction, AuctionReport
from chainBid.celery import app
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

UserModel = get_user_model()


@app.task
def close_auction(pk):
    """
    Auction asynchronous task.
    Executed when the maximum closing date occurs or a user wins.
    """

    auction = get_object_or_404(Auction, pk=pk)
    auction.close_auction()
    AuctionReport.objects.create(auction=auction)


@app.task
def open_auction(pk):
    """
    Auction asynchronous task.
    Executed when the opening date occurs.
    """

    auction = get_object_or_404(Auction, pk=pk)
    max_closing_date = auction.open_auction()
    new_task = close_auction.apply_async((pk,), eta=max_closing_date).id
    auction.add_close_auction_task(task_id=new_task)
