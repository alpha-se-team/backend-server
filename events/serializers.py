from rest_framework import serializers

from .models import Event


class EventSerializer(serializers.ModelSerializer):
    title = serializers.CharField(max_length = 128, allow_blank=False, required=False)
    text = serializers.CharField(allow_blank=True, required=False)
    # img = serializers.ImageField()

    class Meta:
        model = Event
        fields = ['id', 'title', 'text', 'created_at', 'updated_at']


class CreateEventSerializer(serializers.ModelSerializer):
    title = serializers.CharField(max_length = 128, allow_blank=False, required=True)
    text = serializers.CharField(allow_blank=True, required=False)
    # img = serializers.ImageField()

    class Meta:
        model = Event
        fields = ['id', 'title', 'text', 'created_at', 'updated_at']
