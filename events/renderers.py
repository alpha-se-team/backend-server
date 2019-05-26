import json

from rest_framework.renderers import JSONRenderer


class ListEventsJSONRenderer(JSONRenderer):
    charset = 'utf-8'

    def render(self, data, media_type=None, renderer_context=None):
        return json.dumps({'events': data})


class EventJSONRenderer(JSONRenderer):
    charset = 'utf-8'

    def render(self, data, media_type=None, renderer_context=None):
        errors = data.pop('errors', None)

        if errors is not None:
            # Send the error under `event` namespace
            data['event'] = errors
            return super(EventJSONRenderer, self).render(data)

        return json.dumps({'event': data})
