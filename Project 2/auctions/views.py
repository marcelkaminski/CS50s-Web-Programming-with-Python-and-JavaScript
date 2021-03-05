from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import User, Auction
from .forms import NewAuctionForm


def index(request):
    auctions = Auction.objects.all()
    return render(request, "auctions/index.html", {"auctions": auctions})


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


def auction(request, auctionID):
    auction = Auction.objects.get(id=auctionID)
    return render(request, "auctions/auction.html", {"auction": auction})


@login_required
def add(request):
    if request.method == "GET":
        return render(request, "auctions/add.html", {"form": NewAuctionForm})
    elif request.method == "POST":
        user = User.objects.get(username=request.user)
        form = NewAuctionForm(request.POST)
        if form.is_valid():
            auction = form.save(commit=False)
            auction.owner = user
            auction.save()
            return HttpResponseRedirect(f"/auction/{auction.id}")
        else:
            return render(request, "auctions/add.html", {"form": form})
