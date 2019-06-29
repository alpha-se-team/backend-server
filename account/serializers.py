from rest_framework import serializers
from rest_framework.serializers import raise_errors_on_nested_writes
from rest_framework.utils import model_meta

from .models import Plan, Profile, ProfileStats
from .exceptions import PlanDoesNotExist


class PlanSerializer(serializers.ModelSerializer):
    title = serializers.CharField(max_length=128,
                                  allow_blank=False,
                                  required=False)
    description = serializers.CharField(allow_blank=True, required=False)
    total_bandwidth = serializers.IntegerField()

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
    username = serializers.CharField(source='user.username', required=False)
    plan_id = serializers.IntegerField(source='active_plan.id', required=False)

    def update(self, instance, validated_data):
        raise_errors_on_nested_writes('update', self, validated_data)
        info = model_meta.get_field_info(instance)

        active_plan_id = validated_data.pop('active_plan', None)

        # Simply set each attribute on the instance, and then save it.
        # Note that unlike `.create()` we don't need to treat many-to-many
        # relationships as being a special case. During updates we already
        # have an instance pk for the relationships to be associated with.
        for attr, value in validated_data.items():
            if attr in info.relations and info.relations[attr].to_many:
                field = getattr(instance, attr)
                field.set(value)
            else:
                setattr(instance, attr, value)

        if active_plan_id:
            active_plan_id = active_plan_id['id']
            try :
                plan = Plan.objects.get(pk=active_plan_id)
            except:
                raise PlanDoesNotExist()
            setattr(instance, 'active_plan', plan)

        instance.save()

        return instance

    class Meta:
        model = Profile
        fields = ('username', 'amount_consumed', 'amount_consumed_up',
                  'amount_consumed_down', 'plan_id', 'connected_devices')
        read_only_fields = (
            'username',
            'amount_consumed',
        )


class ProfileStatsSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', required=False)

    class Meta:
        model = ProfileStats
        fields = '__all__'
        read_only_fields = ('user', 'date', 'amount_consumed_down',
                            'amount_consumed_up')
