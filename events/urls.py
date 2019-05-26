from django.urls import path

from .views import (EventRetriveUpdateAPIView, EventsRetriveAPIView,
                    EventCreateAPIView)

app_name = 'events'

urlpatterns = [
    path('event/all/', EventsRetriveAPIView.as_view(), name='list events'),
    path('event/', EventCreateAPIView.as_view(), name='create event'),
    path('event/<int:pk>/',
         EventRetriveUpdateAPIView.as_view(),
         name='retrive-update event'),
    path('event/', EventsRetriveAPIView.as_view(), name='list events'),
]
