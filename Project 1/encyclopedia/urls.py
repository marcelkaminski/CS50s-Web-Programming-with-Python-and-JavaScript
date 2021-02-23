from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("page/<str:title>", views.getEntryPage, name="getEntryPage"),
    path("random/", views.getRandomPage, name="getRandomPage"),
    path("search/", views.getSearchPage, name="getSearchPage"),
    path("add/", views.createNewPage, name="createNewPage")
]
