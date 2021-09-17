from auctions.models import Auction
from auctions.tasks import start_auction
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone


@receiver(post_save, sender=Auction)
def start_auction_handler(sender, instance, created, **kwargs):
    """
    Set the start_auction () task to run on the auction's opening_date with Celery.
    """

    now = timezone.now()
    if instance.opening_date:
        if now < instance.opening_date and not instance.status:
            start_auction.apply_async((instance.pk,), eta=instance.opening_date)
