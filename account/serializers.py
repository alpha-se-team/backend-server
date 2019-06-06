from rest_framework import serializers

from .models import Plan


class PlanSerializer(serializers.ModelSerializer):
    title = serializers.CharField(max_length=128,
                                  allow_blank=False,
                                  required=True)
    text = serializers.CharField(allow_blank=True, required=False)

    class Meta:
        model = Plan
        fields = '__all__'
