from django.urls import path

from .views import (PlanRetrieveUpdateDestroyAPIView, PlansRetriveAPIView,
                    PlanCreateAPIView, ProfileRetrieveUpdateAPIView,
                    ConnectDeviceAPIView, DisconnectDeviceAPIView,
                    DisconnectAllDevicesAPIView)

app_name = 'account'

urlpatterns = [
    path('plan/all/', PlansRetriveAPIView.as_view(), name='list all plans'),
    path('plan/<int:pk>/', PlanRetrieveUpdateDestroyAPIView.as_view(), name='retrieve-update-destory plan'),
    path('plan/', PlanCreateAPIView.as_view(), name='create plan'),

    path('profile/', ProfileRetrieveUpdateAPIView.as_view(), name='retrieve-update profile'),

    path('profile/connection/connect/', ConnectDeviceAPIView.as_view(), name='connect-device profile'),
    path('profile/connection/disconnect/', DisconnectDeviceAPIView.as_view(), name='disconnect-device profile'),
    path('profile/connection/disconnect_all/', DisconnectAllDevicesAPIView.as_view(), name='disconnect-all-devices profile'),
]
