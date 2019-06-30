import json

from rest_framework.renderers import JSONRenderer
from core.renderers import BasicJSONRenderer, BasicListJSONRenderer



class ListPlansJSONRenderer(BasicListJSONRenderer):
    object_label_plural = 'plans'


class PlanJSONRenderer(BasicJSONRenderer):
    object_label = 'plan'

class ProfileJSONRenderer(BasicJSONRenderer):
    object_label = 'profile'


class ListProfileStatsJSONRenderer(BasicListJSONRenderer):
    object_label_plural = 'profile_stats'
