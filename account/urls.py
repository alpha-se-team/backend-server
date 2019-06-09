from django.urls import path

from .views import (PlanRetrieveUpdateDestroyAPIView, PlansRetriveAPIView,
                    PlanCreateAPIView, ProfileRetrieveAPIView)

app_name = 'account'

urlpatterns = [
    path('plan/all/', PlansRetriveAPIView.as_view(), name='list all plans'),
    path('plan/<int:pk>/', PlanRetrieveUpdateDestroyAPIView.as_view(), name='retrieve-update-destory plan'),
    path('plan/', PlanCreateAPIView.as_view(), name='create plan'),

    path('profile/<str:username>/', ProfileRetrieveAPIView.as_view(), name='retrieve profile')
]
