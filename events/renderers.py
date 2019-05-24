import json

from rest_framework.renderers import JSONRenderer


class EventJSONRenderer(JSONRenderer):
    charset = 'utf-8'

    def render(self, data, media_type=None, renderer_context=None):
        # errors = data.pop('errors')

        # if errors is not None:
        #     # Send the error under `events` namespace
        #     data['events'] = errors
        #     return super(EventJSONRenderer, self).render(data)

        return json.dumps({'event': data})


class EventsJSONRenderer(JSONRenderer):
    charset = 'utf-8'

    def render(self, data, media_type=None, renderer_context=None):
        return json.dumps({'events': data})
