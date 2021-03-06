from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("auction/<int:auctionID>", views.auction, name="auction"),
    path("auction/<int:auctionID>/bid", views.bid, name="bid"),
    path("auction/<int:auctionID>/close", views.close, name="close"),
    path("auction/<int:auctionID>/comment", views.comment, name="comment"),
    path("add", views.add, name="add"),
    path("watchlist", views.watchlist, name="watchlist")
]
