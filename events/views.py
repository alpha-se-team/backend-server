import json

from django.shortcuts import render

from rest_framework import status
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny
from rest_framework.authentication import BasicAuthentication
from rest_framework.generics import (
    CreateAPIView,
    RetrieveAPIView,
    RetrieveUpdateAPIView,
    ListAPIView,
)

from .models import Event
from .renderers import (
    EventJSONRenderer,
    ListEventsJSONRenderer,
)
from .serializers import (EventSerializer, CreateEventSerializer,
                          ImageEventSerializer)

from core.renderers import ImageJSONRenderer

# import six

from drf_yasg.utils import swagger_auto_schema
import drf_yasg.openapi as openapi


class ImageEventRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    permission_classes = (AllowAny, )
    authentication_classes = (BasicAuthentication, )
    renderer_classes = (ImageJSONRenderer, )
    serializer_class = ImageEventSerializer
    queryset = Event.objects.all()

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        data = request.data.get('img', {})  # get by namespace
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(
            {self.get_renderers()[0].object_label: "Image updated."})


class EventsRetrieveAPIView(ListAPIView):
    permission_classes = (AllowAny, )
    authentication_classes = (BasicAuthentication, )
    renderer_classes = (ListEventsJSONRenderer, )
    serializer_class = EventSerializer
    queryset = Event.objects.all()


class EventCreateAPIView(CreateAPIView):
    permission_classes = (AllowAny, )
    # authentication_classes
    renderer_classes = (EventJSONRenderer, )
    serializer_class = CreateEventSerializer

    # @swagger_auto_schema(
    #                      manual_parameters=[
    #                          openapi.Parameter('serial', openapi.IN_QUERY,  type=openapi.TYPE_STRING, example="785343")
    #                      ],
    #                      responses={ 200:  {
    #                          openapi.Schema(type="object",  properties={ 'device_serial': openapi.Schema(type="string", example="785343") } )
    #                      }
    #                      })
    def post(self, request, *args, **kwargs):
        return self.create(request, args, kwargs)

    def create(self, request, *args, **kwargs):
        event = request.data.get('event', None)
        if event is None:
            raise NotFound("Event key not found.")
        serializer = self.get_serializer(data=event)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data,
                        status=status.HTTP_201_CREATED,
                        headers=headers)


class EventRetrieveUpdateAPIView(RetrieveAPIView):
    permission_classes = (IsAuthenticatedOrReadOnly, )
    renderer_classes = (EventJSONRenderer, )
    serializer_class = EventSerializer
    queryset = Event.objects.all()

    def retrieve(self, request, *args, **kargs):
        pk = kargs.get('pk', None)
        if pk is not None:
            queryset = Event.objects.filter(id=pk)
            if not queryset.exists():
                raise NotFound("No such event found.")
            event = queryset.get(pk=pk)
            serializer = self.serializer_class(event)
            return Response(serializer.data, status=status.HTTP_200_OK)
        raise NotFound("No pk supplied.")

    # def update(self, request, *args, **kwargs):
    #     serializer_data = request.data.get('event', {})
    #     serializer = self.serializer_class(request.user,
    #                                        data=serializer_data,
    #                                        partial=True)
    #     serializer.is_valid(raise_exception=True)
    #     serializer.save()
    #     return Response(serializer.data, status=status.HTTP_200_OK)
