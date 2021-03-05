from django.forms import ModelForm

from .models import *


class NewAuctionForm(ModelForm):
    class Meta:
        model = Auction
        fields = ['title', 'description', 'category', 'price', 'imageURL']


class NewBidForm(ModelForm):
    class Meta:
        model = Bid
        fields = ['price']
