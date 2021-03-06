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
    price = models.DecimalField(max_digits=5, decimal_places=2)
    bids = models.ManyToManyField('Bid', blank=True, related_name="bids")
    date = models.DateTimeField(default=timezone.now)
    imageURL = models.URLField(default="https://user-images.githubusercontent.com/16052233/61581543-f688b100-ab1f-11e9-86b1-023decba19ac.png")
    active = models.BooleanField(default=True)
    comments = models.ManyToManyField('Comment', blank=True, related_name="comments")

    def __str__(self):
        return f"{self.owner}/{self.title}"


class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="watchlist")
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE, related_name="listings")

    def __str__(self):
        return f"{self.user.username} add {self.auction.title} to watchlist"


class Bid(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="userBids")
    price = models.DecimalField('New Bid ', max_digits=5, decimal_places=2)
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.user} put a bid in for {self.price}"

    class Meta:
        get_latest_by = ['date']


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="userComments")
    title = models.CharField(max_length=32, default="")
    comment = models.TextField(max_length=255)
    time = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.user}: {self.comment}"
