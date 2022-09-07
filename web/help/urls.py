from django.contrib import admin
from django.urls import path

# importing views from views..py
from help.views import get_started_view

app_name = 'help'

urlpatterns = [
    path('get-started/', get_started_view, name='get_started'),
    path('how-to-search/', get_started_view, name='how_to_search'),
    path('explore-entry/', get_started_view, name='explore_entry'),
]