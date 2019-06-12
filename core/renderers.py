import json

from rest_framework.renderers import JSONRenderer


class BasicJSONRenderer(JSONRenderer):
    charset = 'utf-8'
    object_label = 'object'

    def render(self, data, media_type=None, renderer_context=None):
        errors = data.pop('errors', None)

        if errors is not None:
            # Send the error under `plan` namespace
            data[self.object_label] = errors
            return super(BasicJSONRenderer, self).render(data)

        return json.dumps({self.object_label: data})


class ImageJSONRenderer(BasicJSONRenderer):
    object_label = 'img'
