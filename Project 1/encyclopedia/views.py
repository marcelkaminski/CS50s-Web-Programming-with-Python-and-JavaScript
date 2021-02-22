from django.shortcuts import render
from django.http import HttpResponseRedirect

from . import util
from random import choice
from markdown2 import markdown

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def getEntryPage(request, title):
    return render(request, "encyclopedia/entryPage.html", {
        "title": title,
        "entry": markdown(util.get_entry(title))
    })


def getRandomPage(request):
    title = choice(util.list_entries())
    return HttpResponseRedirect(f"page/{title}")
