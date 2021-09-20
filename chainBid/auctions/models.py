from django.contrib.auth import get_user_model
from django.db import models

UserModel = get_user_model()


class Auction(models.Model):
    """
    Auction model.

    :fields
    - final_price: This filed will be populated only at the end of the auction.
    - status: False=non active, True=active.
    - won_by: This filed will be populated only at the end of the auction.
    """

    title = models.CharField(max_length=50)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(blank=True, null=True)
    initial_price = models.DecimalField(max_digits=11, decimal_places=2, blank=True, null=True)
    final_price = models.DecimalField(max_digits=11, decimal_places=2, blank=True, null=True)
    opening_date = models.DateTimeField(blank=True, null=True)
    closing_date = models.DateTimeField(blank=True, null=True)
    status = models.BooleanField(default=False)
    won_by = models.ForeignKey(UserModel, on_delete=models.SET_NULL, related_name='auctions', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Auction'
        verbose_name_plural = 'Auctions'
        ordering = ['-opening_date', 'title']

    def __str__(self):
        return self.title

    def toggle_status(self):
        if self.status:
            self.status = False
        else:
            self.status = True
        self.save()
