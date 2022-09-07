from django.shortcuts import render


def get_started_view(request):
    return render(request, "get_started.html")


def how_to_search_view(request):
    return render(request, "how_to_search.html")


def explore_entry_view(request):
    return render(request, "explore_entry.html")
