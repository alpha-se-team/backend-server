from django.urls import path

from .views import PlanRetrieveUpdateDestroyAPIView , PlansRetriveAPIView

app_name = 'account'

urlpatterns = [
    path('account/plan/all/', PlansRetriveAPIView.as_view(), name='list all plans'),
    path('account/plan/', PlanRetrieveUpdateDestroyAPIView.as_view(), name='retrive-update-destory plan'),


]
