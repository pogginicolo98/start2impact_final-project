from auctions.models import Auction
from auctions.tasks import close_auction, open_auction
from chainBid.celery import app
from django.db.models.signals import post_save
from django.dispatch import receiver, Signal
from django.utils import timezone

# Creating custom signal for view: AuctionBidAPIView
auction_bid_apiview_called = Signal(providing_args=['instance'])


@receiver(post_save, sender=Auction)
def open_auction_handler(sender, instance, created, **kwargs):
    """
    Set the open_auction() task to run on the auction's opening date.
    """

    now = timezone.now()
    if instance.opened_at and instance.initial_price:
        if now < instance.opened_at and not instance.status:
            open_auction.apply_async((instance.pk,), eta=instance.opened_at)


def update_bid_closing_time(sender, instance, **kwargs):
    """
    When a new bid is placed, the last celery task that is handling the closing of the auction is revoked and
    a new one is created with 15 seconds of countdown.
    """

    task = instance.pop_task()
    if task is not None:
        app.control.revoke(task['task_id'], terminate=True, signal='SIGKILL')
    eta = timezone.now() + timezone.timedelta(seconds=15)
    task_id = close_auction.apply_async((instance.pk,), eta=eta).id
    instance.push_task(task_id=task_id, eta=eta)


# Connecting custom signals for views: AuctionBidAPIView
auction_bid_apiview_called.connect(update_bid_closing_time)
