from auctions.models import Auction
from chainBid.celery import app
from django.shortcuts import get_object_or_404


@app.task
def start_auction(pk):
    """
    Auction asynchronous task.
    When the opening_date occurs, the auction toggle its status to enabled.
    """

    auction = get_object_or_404(Auction, pk=pk)
    auction.toggle_status()

# from django.contrib.auth import get_user_model
# UserModel = get_user_model()
# user = UserModel.objects.get(pk=user_id)
