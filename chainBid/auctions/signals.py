from auctions.models import Auction
from auctions.tasks import start_auction
from django.db.models.signals import post_save
from django.dispatch import receiver


@receiver(post_save, sender=Auction)
def start_auction_handler(sender, instance, created, **kwargs):
    """
    ???
    """

    if created:
        start_auction.apply_async((instance,), eta=instance.opening_date)
