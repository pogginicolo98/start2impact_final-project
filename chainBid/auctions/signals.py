from auctions.models import Auction, AuctionReport
from auctions.tasks import open_auction
from chainBid.celery import app
from django.db.models.signals import post_save, pre_delete, pre_save
from django.dispatch import receiver
from django.utils import timezone
from django.utils.text import slugify
from utils.auction_redis import clean_db, get_latest_object_on_redis, record_object_on_redis, TASKS_KEY
from utils.randomics import generate_random_string, random_date


@receiver(pre_save, sender=Auction)
def set_auction_slug(sender, instance, *args, **kwargs):
    """
    Set the auction slug when a new auction is created.
    """

    if instance and not instance.slug:
        slug = slugify(instance.title)
        random_string = generate_random_string()
        instance.slug = f"{slug}-{random_string}"


@receiver(post_save, sender=Auction)
def open_auction_handler(sender, instance, created, **kwargs):
    """
    Set the open_auction() task to run on the auction's opening date.
    """

    now = timezone.now()
    if instance.opened_at and instance.initial_price:
        if now < instance.opened_at and not instance.status:
            if not created:
                previous_task = get_latest_object_on_redis(auction=instance.slug, type_obj=TASKS_KEY)
                if previous_task is not None:
                    if previous_task.get('task_id', None):
                        app.control.revoke(previous_task['task_id'], terminate=True, signal='SIGKILL')
            min_duration = instance.opened_at + timezone.timedelta(weeks=20)
            max_duration = instance.opened_at + timezone.timedelta(weeks=24)
            max_closing_date = random_date(start=min_duration, end=max_duration)
            open_auction_task = open_auction.apply_async((instance.slug, max_closing_date), eta=instance.opened_at).id
            record_object_on_redis(auction=instance.slug, task_id=open_auction_task)


@receiver(pre_delete, sender=Auction)
def delete_auction_handler(sender, instance, **kwargs):
    """
    Abort tasks associated with an auction when it is deleted.
    """

    current_task = get_latest_object_on_redis(auction=instance.slug, type_obj=TASKS_KEY)
    if current_task is not None:
        if current_task.get('task_id', None):
            app.control.revoke(current_task['task_id'], terminate=True, signal='SIGKILL')
    clean_db(auction=instance.slug)


@receiver(post_save, sender=AuctionReport)
def make_report_handler(sender, instance, created, **kwargs):
    """
    Make an auction report and write it on the Ethereum blockchain.
    """

    if created:
        instance.make_report()
