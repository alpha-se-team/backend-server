from rest_framework import serializers

from .models import Plan


class PlanSerializer(serializers.ModelSerializer):
    title = serializers.CharField(max_length=128,
                                  allow_blank=False,
                                  required=False)
    description = serializers.CharField(allow_blank=True, required=False)

    class Meta:
        model = Plan
        fields = '__all__'


class CreatePlanSerializer(serializers.ModelSerializer):
    title = serializers.CharField(max_length=128,
                                  allow_blank=False,
                                  required=True)
    description = serializers.CharField(allow_blank=True, required=False)
    total_bandwidth = serializers.IntegerField(required=True)

    class Meta:
        model = Plan
        fields = '__all__'
