from rest_framework import serializers

from .models import Plan, Profile


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


class ProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username')
    plan_id = serializers.ReadOnlyField(source='active_plan.id')

    class Meta:
        model = Profile
        fields = ('username', 'amount_consumed', 'plan_id')
        read_only_fields = ('username', 'plan_id')
