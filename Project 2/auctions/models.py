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

    def __str__(self):
        return f"{self.owner}/{self.title}"
