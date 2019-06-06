# from django.shortcuts import render

from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny
from rest_framework.authentication import BasicAuthentication
from rest_framework.generics import (
    # CreateAPIView,
    # RetrieveAPIView,
    # RetrieveUpdateAPIView,
    RetrieveUpdateDestroyAPIView,
    ListAPIView,
)


from .models import Plan, Profile
from .renderers import PlanJSONRenderer, ListPlansJSONRenderer
from .serializers import PlanSerializer


class PlanRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    permission_classes = IsAuthenticatedOrReadOnly
    renderer_classes = (PlanJSONRenderer,)
    serializer_class = PlanSerializer
    queryset = Plan.objects.all()


class PlansRetriveAPIView(ListAPIView):
    permission_classes = (AllowAny,)
    authentication_classes = (BasicAuthentication, )
    renderer_classes = (ListPlansJSONRenderer,)
    serializer_class = PlanSerializer
    queryset = Plan.objects.all()
