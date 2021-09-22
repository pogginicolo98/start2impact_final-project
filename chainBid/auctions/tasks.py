from auctions.models import Auction
from chainBid.celery import app
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

UserModel = get_user_model()


@app.task
def close_auction(pk):
    """
    Auction asynchronous task.

    When the maximum closing date occurs or a user wins, perform the following actions:
    1) Disable the auction.
    2) Store the winning bid's data.
    3) Remove bids data from Redis.
    4) Make a report.
    5) Write the report on the Ethereum blockchain.
    """

    auction = get_object_or_404(Auction, pk=pk)
    auction.close_auction()


@app.task
def open_auction(pk):
    """
    Auction asynchronous task.

    When the opening date occurs, perform the following actions:
    1) Enable the auction.
    2) Set the close_auction() task to run on a random date between 20 to 24 hours after the opening.
    """

    auction = get_object_or_404(Auction, pk=pk)
    max_closing_date = auction.open_auction()
    task_id = close_auction.apply_async((pk,), eta=max_closing_date).id
    auction.push_task_id(task_id)
