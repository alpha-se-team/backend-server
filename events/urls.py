from django.urls import path

from .views import (EventRetrieveUpdateAPIView, EventsRetrieveAPIView,
                    EventCreateAPIView, ImageEventRetrieveUpdateAPIView)

app_name = 'events'

urlpatterns = [
    path('event/all/', EventsRetrieveAPIView.as_view(), name='list events'),
    path('event/', EventCreateAPIView.as_view(), name='create event'),

    path('event/<int:pk>/',
         EventRetrieveUpdateAPIView.as_view(),
         name='retrive-update event'),

    path('event/<int:pk>/image/',
         ImageEventRetrieveUpdateAPIView.as_view(),
         name="retrive-update event's image"),

    path('event/', EventsRetrieveAPIView.as_view(), name='list events'),
]
