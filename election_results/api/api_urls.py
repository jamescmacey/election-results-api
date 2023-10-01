from django.urls import path

from .views import EventList, ResultsList, Event
urlpatterns = [
    path("<str:event_id>/results", ResultsList.as_view(), name="results_list"),
    path("<str:event_id>", Event.as_view(), name="event"),
    path("", EventList.as_view(), name="event_list"),
]