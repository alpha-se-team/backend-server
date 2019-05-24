from django.urls import path

from .views import EventRetriveUpdateAPIView, EventsRetriveAPIView

app_name = 'events'

urlpatterns = [
    path('event/all/', EventsRetriveAPIView.as_view(), name='list events'),
    path('event/<int:pk>/', EventRetriveUpdateAPIView.as_view(), name='retrive-update event'),
    path('event/', EventsRetriveAPIView.as_view(), name='list events'),
]
