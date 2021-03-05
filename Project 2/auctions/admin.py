from django.contrib import admin
from .models import User, Category, Auction, Watchlist, Bid

# Register your models here.
admin.site.register(User)
admin.site.register(Category)
admin.site.register(Auction)
admin.site.register(Watchlist)
admin.site.register(Bid)