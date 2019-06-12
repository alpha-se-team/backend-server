import json

from rest_framework.renderers import JSONRenderer
from core.renderers import BasicJSONRenderer


class ListEventsJSONRenderer(JSONRenderer):
    charset = 'utf-8'

    def render(self, data, media_type=None, renderer_context=None):
        return json.dumps({'events': data})


class EventJSONRenderer(BasicJSONRenderer):
    object_label = 'event'
