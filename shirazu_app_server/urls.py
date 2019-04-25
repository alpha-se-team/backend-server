""" URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path

from rest_framework import permissions

from drf_yasg.views import get_schema_view
from drf_yasg import openapi
# from rest_framework.authtoken.views import obtain_auth_token

schema_view = get_schema_view(
    openapi.Info(title="Shirazu-mockserver API",
                 default_version='v1',
                 description="Go crazy!",
                 terms_of_service="https://www.google.com/policies/terms/",
                 contact=openapi.Contact(email="alifarazdaghi@gmail.com"),
                 license=openapi.License(
                     name="GPLv3",
                     url='https://www.gnu.org/licenses/gpl-3.0.en.html')),
    public=True,
    permission_classes=(permissions.AllowAny, ),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    re_path('^swagger(?P<format>\.json|\.yaml)$',
            schema_view.without_ui(cache_timeout=0),
            name='schema-json'),
    path('swagger/',
         schema_view.with_ui('swagger', cache_timeout=0),
         name='schema-swagger-ui'),
    path('redoc/',
         schema_view.with_ui('redoc', cache_timeout=0),
         name='schema-redoc'),

    # path('apiv1/auth', obtain_auth_token),
    path('apiv1/', include('authentication.urls', namespace='authentication')),
]
