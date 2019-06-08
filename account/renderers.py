import json

from rest_framework.renderers import JSONRenderer


class ListPlansJSONRenderer(JSONRenderer):
    charset = 'utf-8'

    def render(self, data, media_type=None, renderer_context=None):
        return json.dumps({'plans': data})


class PlanJSONRenderer(JSONRenderer):
    charset = 'utf-8'

    def render(self, data, media_type=None, renderer_context=None):
        print(data)
        errors = data.pop('errors', None)

        if errors is not None:
            # Send the error under `plan` namespace
            data['plan'] = errors
            return super(PlanJSONRenderer, self).render(data)

        return json.dumps({'plan': data})
