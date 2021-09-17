from auctions.models import Auction
from chainBid.celery import app
from django.shortcuts import get_object_or_404

import logging

@app.task
def start_auction(pk):
    """
    Valutare il try/except
    import logging
    logging.warning("Tried to send verification email to non-existing user '%s'" % user_id)
    """

    auction = get_object_or_404(Auction, pk=pk)
    auction.toggle_status()
    # logging.warning(str(auction))

# from django.contrib.auth import get_user_model
# UserModel = get_user_model()
# user = UserModel.objects.get(pk=user_id)
# {% load render_bundle from webpack_loader %}
# {% render_bundle 'app' %}