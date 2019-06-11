import json

from rest_framework.renderers import JSONRenderer
from core.renderers import BasicJSONRenderer



class ListPlansJSONRenderer(JSONRenderer):
    charset = 'utf-8'

    def render(self, data, media_type=None, renderer_context=None):
        return json.dumps({'plans': data})


class PlanJSONRenderer(BasicJSONRenderer):
    object_label = 'plan'


class ProfileJSONRenderer(BasicJSONRenderer):
    object_label = 'profile'
