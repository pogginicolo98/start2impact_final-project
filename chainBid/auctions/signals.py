from auctions.models import Auction, AuctionReport
from auctions.tasks import open_auction
from chainBid.celery import app
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from django.utils import timezone
from utils.auction_redis import clean_db, get_latest_object_on_redis, record_object_on_redis, TASKS_KEY
from utils.randomics import random_date


@receiver(post_save, sender=Auction)
def open_auction_handler(sender, instance, created, **kwargs):
    """
    Set the open_auction() task to run on the auction's opening date.
    """

    now = timezone.now()
    if instance.opened_at and instance.initial_price:
        if now < instance.opened_at and not instance.status:
            if not created:
                previous_task = get_latest_object_on_redis(auction=instance.pk, type_obj=TASKS_KEY)
                if previous_task is not None:
                    if previous_task.get('task_id', None):
                        app.control.revoke(previous_task['task_id'], terminate=True, signal='SIGKILL')
            min_duration = instance.opened_at + timezone.timedelta(seconds=20)
            max_duration = instance.opened_at + timezone.timedelta(seconds=24)
            max_closing_date = random_date(start=min_duration, end=max_duration)
            open_auction_task = open_auction.apply_async((instance.pk, max_closing_date), eta=instance.opened_at).id
            record_object_on_redis(auction=instance.pk, task_id=open_auction_task)


@receiver(pre_delete, sender=Auction)
def delete_auction_handler(sender, instance, **kwargs):
    """
    Abort tasks associated with an auction when it is deleted.
    """

    current_task = get_latest_object_on_redis(auction=instance.pk, type_obj=TASKS_KEY)
    if current_task is not None:
        if current_task.get('task_id', None):
            app.control.revoke(current_task['task_id'], terminate=True, signal='SIGKILL')
    clean_db(auction=instance.pk)


@receiver(post_save, sender=AuctionReport)
def make_report_handler(sender, instance, created, **kwargs):
    """
    Make an auction report and write it on the Ethereum blockchain.
    """

    if created:
        instance.make_report()
