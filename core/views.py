from abc import ABCMeta, abstractmethod

from rest_framework.response import Response
from rest_framework.generics import RetrieveUpdateAPIView

from .renderers import ImageJSONRenderer


class ImageRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    renderer_classes = (ImageJSONRenderer, )
    # serializer_class = None
    # queryset = None

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        data = request.data.get('img', {})  # get by namespace
        instance = self.get_object()
        serializer = self.get_serializer_class()(instance, data=data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(
            {self.get_renderers()[0].object_label: "Image updated."})
