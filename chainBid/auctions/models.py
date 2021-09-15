from django.db import models
from users.models import CustomUser


class Auction(models.Model):
    """
    ???
    """

    title = models.CharField(max_length=50)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(blank=True, null=True)
    opening_price = models.DecimalField(max_digits=11, decimal_places=2)
    closing_price = models.DecimalField(max_digits=11, decimal_places=2, blank=True, null=True)
    opening_date = models.DateTimeField(blank=True, null=True)
    closing_date = models.DateTimeField(blank=True, null=True)
    status = models.BooleanField(default=False)
    won_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, related_name='auctions_won', blank=True, null=True)
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='auctions_created')

    class Meta:
        verbose_name = 'Auction'
        verbose_name_plural = 'Auctions'
        ordering = ['-opening_date', 'title']

    def __str__(self):
        return self.title


# class Bid(models.Model):
#     """
#     ???
#     """
#
#     user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='bids')
#     auction = models.ForeignKey(Auction, on_delete=models.CASCADE, related_name='bids')
#     price = models.DecimalField(max_digits=11, decimal_places=2)
#     created_at = models.DateTimeField(auto_now=True)
#
#     class Meta:
#         verbose_name = 'Bid'
#         verbose_name_plural = 'Bids'
#         ordering = ['auction', '-created_at']
#
#     def __str__(self):
#         return f'{self.auction} - {self.price}'
