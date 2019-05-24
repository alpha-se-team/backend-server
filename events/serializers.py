from rest_framework import serializers

from .models import Event


class EventSerializer(serializers.ModelSerializer):
    # title = serializers.CharField(max_length = 128)

    class Meta:
        model = Event
        fields = ['title', 'text', 'created_at', 'updated_at']
