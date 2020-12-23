from django.shortcuts import render
from django.views.defaults import page_not_found
from django.http import HttpResponse

from . import util

from markdown2 import Markdown

markdowner = Markdown()

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    if not util.get_entry(title):
        return page_not_found(request, True, template_name="404.html")
    return render(request, "encyclopedia/entry.html", {
        "title": title.capitalize(),
        "entry": markdowner.convert(util.get_entry(title))
    })

def search(request):
    """ Search for an wiki entry.
        If the query matches the name of an wiki entry, the user gets redirected to that entry’s page.
        If the query does not match the name of an wiki entry, takes the user to a search results page
        that displays a list of all wiki entries
    """
    query = request.GET.get('q', '') #The empty string handles an empty "request"
    if query:
        queryset = (Q(text_icontains = query))
        results = Posts.objects.filter(queryset).distinct()
    else:
        results = []
    return render(request, 'home.html', {'results':results, 'query':query})

    