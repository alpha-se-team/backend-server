from django.urls import path
from django.views.decorators.csrf import csrf_exempt as _

from .views import (
    RegistrationAPIView,
    LoginAPIView,
    UserRetrieveUpdateAPIView,
    ImageUserRetrieveUpdateAPIView
)

app_name = 'authentication'

urlpatterns = [
    path('user/', _(UserRetrieveUpdateAPIView.as_view()), name='retrive-update user'),
    path('user/image/', _(ImageUserRetrieveUpdateAPIView.as_view()), name='retrive-update user\'s image'),
    path('users/', _(RegistrationAPIView.as_view()), name='register user'),
    path('users/login/', _(LoginAPIView.as_view()), name='login user'),
]
