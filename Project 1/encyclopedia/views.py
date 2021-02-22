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


def getSearchResult(query):
    results = []
    list = util.list_entries()
    for s in list:
        if query in s.lower():
            results.append(s)
    return results


def getSearchPage(request):
    if request.method == 'GET':
        query = request.GET.get('q')
    query = query.lower()
    results = getSearchResult(query)
    if len(results) == 1 and query == results[0].lower():
        return HttpResponseRedirect(f"/page/{results[0]}")
    else:
        return render(request, "encyclopedia/searchPage.html", {
            "query": query,
            "results": results
        })
