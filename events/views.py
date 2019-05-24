from django.shortcuts import render

from rest_framework import status
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny
from rest_framework.authentication import BasicAuthentication
from rest_framework.generics import (
    CreateAPIView,
    RetrieveUpdateAPIView,
    ListAPIView,
)

from .models import Event
from .renderers import (EventJSONRenderer, ListEventsJSONRenderer)
from .serializers import EventSerializer, CreateEventSerializer

from drf_yasg.utils import swagger_auto_schema


class EventsRetriveAPIView(ListAPIView):
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


class EventRetriveUpdateAPIView(RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticatedOrReadOnly, )
    renderer_classes = (EventJSONRenderer, )
    serializer_class = EventSerializer
    queryset = Event.objects.all()

    def retrieve(self, request, *args, **kargs):  # refactor
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
