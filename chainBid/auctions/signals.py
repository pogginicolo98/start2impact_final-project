from auctions.models import Auction, AuctionReport
from auctions.tasks import close_auction, open_auction
from chainBid.celery import app
from django.db.models.signals import post_save, pre_delete
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
            if not created:
                previous_task = instance.get_latest_object_on_redis(type_obj='schedule')
                if previous_task is not None:
                    app.control.revoke(previous_task['task_id'], terminate=True, signal='SIGKILL')
            new_task = open_auction.apply_async((instance.pk,), eta=instance.opened_at).id
            instance.record_object_on_redis(schedule_id=new_task)


@receiver(pre_delete, sender=Auction)
def delete_auction_handler(sender, instance, **kwargs):
    """
    Abort tasks associated with an auction when it is deleted.
    """

    schedule_task = instance.get_latest_object_on_redis(type_obj='schedule')
    if schedule_task is not None:
        app.control.revoke(schedule_task['task_id'], terminate=True, signal='SIGKILL')
    close_auction_task = instance.get_latest_object_on_redis(type_obj='close')
    if close_auction_task is not None:
        app.control.revoke(close_auction_task['task_id'], terminate=True, signal='SIGKILL')
    instance.clean_db()


@receiver(post_save, sender=AuctionReport)
def make_report_handler(sender, instance, created, **kwargs):
    """
    Make an auction report and write it on the Ethereum blockchain.
    """

    if created:
        instance.make_report()


def update_bid_closing_time(sender, instance, **kwargs):
    """
    When a new bid is placed, the last celery task that is handling the closing of the auction is revoked and
    a new one is created with 15 seconds of countdown.
    """

    previous_task = instance.get_latest_object_on_redis(type_obj='close')
    if previous_task is not None:
        app.control.revoke(previous_task['task_id'], terminate=True, signal='SIGKILL')
    eta = timezone.now() + timezone.timedelta(minutes=2)
    new_task = close_auction.apply_async((instance.pk,), eta=eta).id
    instance.record_object_on_redis(close_id=new_task, eta=eta)


# Connecting custom signals for views: AuctionBidAPIView
auction_bid_apiview_called.connect(update_bid_closing_time)
