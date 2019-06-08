# from django.shortcuts import render

from rest_framework import status
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny
from rest_framework.authentication import BasicAuthentication
from rest_framework.generics import (
    CreateAPIView,
    # RetrieveAPIView,
    # RetrieveUpdateAPIView,
    RetrieveUpdateDestroyAPIView,
    ListAPIView,
)

from drf_yasg.utils import swagger_auto_schema
# import drf_yasg.openapi as openapi

from .models import Plan, Profile
from .renderers import PlanJSONRenderer, ListPlansJSONRenderer
from .serializers import PlanSerializer, CreatePlanSerializer


class PlanRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticatedOrReadOnly, )
    renderer_classes = (PlanJSONRenderer,)
    serializer_class = PlanSerializer
    queryset = Plan.objects.all()


class PlanCreateAPIView(CreateAPIView):
    permission_classes = (AllowAny, )
    # authentication_classes
    renderer_classes = (PlanJSONRenderer, )
    serializer_class = CreatePlanSerializer

    @swagger_auto_schema(responses={201: serializer_class(many=True)})
    def post(self, request, *args, **kwargs):
        return self.create(request, args, kwargs)

    def create(self, request, *args, **kwargs):
        plan = request.data.get('plan', None)
        if plan is None:
            raise NotFound("Plan key not found.")
        serializer = self.get_serializer(data=plan)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data,
                        status=status.HTTP_201_CREATED,
                        headers=headers)


class PlansRetriveAPIView(ListAPIView): # LIST
    permission_classes = (AllowAny,)
    authentication_classes = (BasicAuthentication, )
    renderer_classes = (ListPlansJSONRenderer,)
    serializer_class = PlanSerializer
    queryset = Plan.objects.all()
