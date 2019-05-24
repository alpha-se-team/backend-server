from django.shortcuts import render

from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import RetrieveUpdateAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny
from rest_framework.authentication import BasicAuthentication

from .models import Event
from .renderers import EventJSONRenderer
from .serializers import EventSerializer

from drf_yasg.utils import swagger_auto_schema


class EventsRetriveAPIView(ListAPIView):
    permission_classes = (AllowAny, )
    authentication_classes = (BasicAuthentication, )
    renderer_classes = (EventJSONRenderer, )
    serializer_class = EventSerializer
    queryset = Event.objects.all()



class EventRetriveUpdateAPIView(RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticatedOrReadOnly, )
    renderer_classes = (EventJSONRenderer, )
    serializer_class = EventSerializer
    queryset = Event.objects.all()

    def retrieve(self, request, *args, **kargs):
        print(request.data)
        serializer = self.serializer_class(request.data)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # def update(self, request, *args, **kwargs):
    #     serializer_data = request.data.get('user', {})
    #     serializer = self.serializer_class(request.user,
    #                                        data=serializer_data,
    #                                        partial=True)
    #     serializer.is_valid(raise_exception=True)
    #     serializer.save()
    #     return Response(serializer.data, status=status.HTTP_200_OK)
