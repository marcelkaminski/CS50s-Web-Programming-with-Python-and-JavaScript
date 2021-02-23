from django.shortcuts import render
from django.http import HttpResponseRedirect
from django import forms
from django.contrib import messages

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
    return HttpResponseRedirect(f"/page/{title}")


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


class CreateNewPageForm(forms.Form):
    newTitle = forms.CharField(label="Title")
    newContent = forms.CharField(widget=forms.Textarea, label="Content")


def createNewPage(request):
    if request.method == 'GET':
        return render(request, "encyclopedia/createNewPage.html", {
            "form": CreateNewPageForm
        })
    elif request.method == 'POST':
        form = CreateNewPageForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['newTitle']
            content = form.cleaned_data['newContent']
            if title.lower() in [entry.lower() for entry in util.list_entries()]:
                messages.add_message(request, messages.WARNING, message=f'Entry "{title}" already exists')
                return render(request, "encyclopedia/createNewPage.html", {"form": CreateNewPageForm})
            else:
                util.save_entry(title, content)
                return HttpResponseRedirect(f"/page/{title}")
        else:
            return render(request, "encyclopedia/createNewPage.html", {"form": CreateNewPageForm})


class EditPageForm(forms.Form):
    newContent = forms.CharField(widget=forms.Textarea, label="Content")


def editPage(request, title):
    oldContent = util.get_entry(title)
    if request.method == 'GET':
        return render(request, "encyclopedia/editPage.html", {"form": EditPageForm({"newContent": oldContent}), "title":title})
    elif request.method == 'POST':
        form = EditPageForm(request.POST)
        if form.is_valid():
            newContent = form.cleaned_data['newContent']
            util.save_entry(title, newContent)
            return HttpResponseRedirect(f"/page/{title}")
        else:
            return render(request, "encyclopedia/editPage.html", {"form": EditPageForm({"content": oldContent}), "title":title})
