# todo/todo_api/urls.py : API urls.py
import django.conf.urls
from django.urls import path, include
from .views import (
    FlightApiSearch,
    FlightApiBook,
    FlightApiDelete
)

urlpatterns = [
    path('search/<str:origin_code>/<str:destination_code>/<str:date>/',FlightApiSearch.as_view()),
    path('seat/book/',FlightApiBook.as_view()),
    path('seat/cancel/<str:booking_num>/',FlightApiDelete.as_view()),
]