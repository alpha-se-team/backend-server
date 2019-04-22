from django.urls import path

from .api import (
    ListUsersProfiles,
    UserLoginView,
    RegisterUserProfileView,
    UserProfileInfoView,
)

urlpatterns = [
    path('auth/all/', ListUsersProfiles.as_view(), name='user-profiles-all'),
    path('auth/login/', UserLoginView.as_view(), name='user-login'),
    path('auth/register/', RegisterUserProfileView.as_view(), name='user-profile-register'),
    path('user/<int:pk>/', UserProfileInfoView.as_view(), name="user-profile-get"),
]
