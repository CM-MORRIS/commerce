from django.contrib.auth.models import AbstractUser
from django.db import models
import django.utils.timezone

# User table already created in migrations folder
class User(AbstractUser):
    pass

class Listings(models.Model):

    listing_id =        models.AutoField(primary_key=True)
    title =             models.CharField(max_length=100)
    description =       models.CharField(max_length=1000)
    starting_price =    models.DecimalField(max_digits=11, decimal_places=2)
    current_price =     models.DecimalField(max_digits=11, decimal_places=2)
    start_date =        models.DateTimeField(auto_now=False, auto_now_add=False, default=django.utils.timezone.now)
    end_date =          models.DateTimeField(auto_now=False, auto_now_add=False, default=django.utils.timezone.now)
    is_sold =           models.BooleanField()

class Bids(models.Model):

    bid_id =        models.AutoField(primary_key=True)
    user_id =       models.ForeignKey(User, on_delete=models.CASCADE)
    listing_id =    models.ForeignKey(Listings, on_delete=models.CASCADE)
    bid_price =     models.DecimalField(max_digits=11, decimal_places=2)

    def __str__(self):
        return f"User: {self.user_id} bid on listing: {self.listing_id} with a price of {self.bid_price}"

class Comments(models.Model):

    comment_id =    models.AutoField(primary_key=True)
    user_id =       models.ForeignKey(User, on_delete=models.CASCADE)
    listing_id =    models.ForeignKey(Listings, on_delete=models.CASCADE)
    comment =       models.CharField(max_length=1000)
