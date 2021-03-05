from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class User(AbstractUser):
    pass


class Category(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.name}"


class Auction(models.Model):
    owner = models.ForeignKey('User', on_delete=models.CASCADE, related_name='auctionsByUser')
    title = models.CharField(max_length=64)
    description = models.TextField()
    category = models.ForeignKey('Category', on_delete=models.CASCADE, related_name='auctionsByCategory')
    startingBid = models.DecimalField(max_digits=5, decimal_places=2)
    date = models.DateTimeField(default=timezone.now)
    imageURL = models.URLField(default="https://user-images.githubusercontent.com/16052233/61581543-f688b100-ab1f-11e9-86b1-023decba19ac.png")

    def __str__(self):
        return f"{self.owner}/{self.title}"


class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="watchlist")
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE, related_name="listings")

    def __str__(self):
        return f"{self.user.username} add {self.auction.title} to watchlist"