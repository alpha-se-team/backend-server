# from django.shortcuts import render

from rest_framework import status
# from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny, IsAuthenticated
from rest_framework.authentication import BasicAuthentication
from rest_framework.generics import (
    GenericAPIView,
    CreateAPIView,
    # RetrieveAPIView,
    RetrieveUpdateAPIView,
    RetrieveUpdateDestroyAPIView,
    ListAPIView,
)

from drf_yasg.utils import swagger_auto_schema
# import drf_yasg.openapi as openapi

from .models import Plan, Profile, ProfileStats
from .renderers import PlanJSONRenderer, ListPlansJSONRenderer, ProfileJSONRenderer, ListProfileStatsJSONRenderer
from .serializers import PlanSerializer, CreatePlanSerializer, ProfileSerializer, ProfileStatsSerializer
from .exceptions import ProfileDoesNotExist


class GenericDeviceAPIView(GenericAPIView):
    permission_classes = (IsAuthenticated, )
    renderer_classes = (ProfileJSONRenderer, )
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()

    def f_(self, profile):
        pass

    def get(self, request):
        username = self.request.user.username
        try:
            profile = Profile.get_by_username(username)
        except Profile.DoesNotExist:
            raise ProfileDoesNotExist

        self.f_(profile)
        serializer = self.get_serializer_class()(profile)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ConnectDeviceAPIView(GenericDeviceAPIView):
    def f_(self, profile):
        profile.add_device()
        profile.save()

class DisconnectDeviceAPIView(GenericDeviceAPIView):
    def f_(self, profile):
        profile.remove_device()
        profile.save()

class DisconnectAllDevicesAPIView(GenericDeviceAPIView):
    def f_(self, profile):
        profile.remove_all_devices()
        profile.save()


class ProfileRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    # permission_classes = (AllowAny, )
    permission_classes = (IsAuthenticated, )
    renderer_classes = (ProfileJSONRenderer, )
    serializer_class = ProfileSerializer
    queryset = ''

    def update(self, request, *args, **kwargs):
        username = self.request.user.username
        partial = kwargs.pop('partial', False)
        data = request.data.get('profile', {})

        # UGLY HACK - readonly fields
        data.pop("username", None)
        data.pop("amount_consumed", None)

        try:
            profile = Profile.objects.select_related('user').get(
                user__username=username)
        except Profile.DoesNotExist:
            raise ProfileDoesNotExist

        serializer = self.get_serializer(profile, data=data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(profile, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the profile.
            profile._prefetched_objects_cache = {}

        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        username = self.request.user.username
        try:
            profile = Profile.objects.select_related('user').get(
                user__username=username)
        except Profile.DoesNotExist:
            raise ProfileDoesNotExist

        serializer = self.get_serializer_class()(profile)

        return Response(serializer.data, status=status.HTTP_200_OK)


class PlanRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    """C[RUD] ops for Plan"""
    permission_classes = (AllowAny, )
    renderer_classes = (PlanJSONRenderer, )
    serializer_class = PlanSerializer
    queryset = Plan.objects.all()

    def update(self, request, *args, **kwargs):
        # print(args, kwargs, request.data, sep='\n')
        data = request.data.get('plan', {})
        partial = kwargs.pop('partial', False)
        pk = kwargs.get('pk', None)
        if pk is not None:
            queryset = Plan.objects.filter(id=pk)
            if not queryset.exists():
                raise NotFound("No such plan found.")
            profile = queryset.get(pk=pk)
            # print(profile)
            serializer = self.get_serializer(profile,
                                             data=data,
                                             partial=partial,
                                             many=False)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)

            if getattr(profile, '_prefetched_objects_cache', None):
                # If 'prefetch_related' has been applied to a queryset, we need to
                # forcibly invalidate the prefetch cache on the instance.
                profile._prefetched_objects_cache = {}

            return Response(serializer.data)
        raise NotFound("No pk supplied.")


class PlanCreateAPIView(CreateAPIView):
    """[C]RUD op for Plan"""
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


class PlansRetriveAPIView(ListAPIView):  # LIST
    """C[R]UD op to list all Plans"""
    permission_classes = (AllowAny, )
    authentication_classes = (BasicAuthentication, )
    renderer_classes = (ListPlansJSONRenderer, )
    serializer_class = PlanSerializer
    queryset = Plan.objects.all()


class ListProfileStatsAPIView(ListAPIView):
    permission_classes = (IsAuthenticated, )
    renderer_classes = (ListProfileStatsJSONRenderer, )
    serializer_class = ProfileStatsSerializer
    queryset = ProfileStats.objects.all()

    model = ProfileStats

    def get_object(self):
        username = self.request.user.username
        queryset = self.filter_queryset(self.get_queryset())

        try:
            obj = self.model.filter_by_username(queryset, username)
        except Profile.DoesNotExist:
            raise ProfileDoesNotExist

        self.check_object_permissions(self.request, obj)
        return obj
