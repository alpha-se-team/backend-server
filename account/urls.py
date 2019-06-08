from django.urls import path

from .views import (PlanRetrieveUpdateDestroyAPIView, PlansRetriveAPIView,
                    PlanCreateAPIView)

app_name = 'account'

urlpatterns = [
    path('account/plan/all/', PlansRetriveAPIView.as_view(), name='list all plans'),
    path('account/plan/<int:pk>', PlanRetrieveUpdateDestroyAPIView.as_view(), name='retrive-update-destory plan'),
    path('account/plan/', PlanCreateAPIView.as_view(), name='create plan'),
]
