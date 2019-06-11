from rest_framework import serializers

from .models import Event
# import six


class Base64Field(serializers.Field):
    def to_representation(self, value):
        # print(value)
        return value.decode('utf-8')

    def to_internal_value(self, data):
        # print(data)
        return data.encode('utf-8')


class ImageEventSerializer(serializers.ModelSerializer):
    img = Base64Field()  # Hackty hack hack

    # img = serializers.ImageField()

    class Meta:
        model = Event
        fields = [
            'img',
        ]


class EventSerializer(serializers.ModelSerializer):
    title = serializers.CharField(max_length=128,
                                  allow_blank=False,
                                  required=False)
    text = serializers.CharField(allow_blank=True, required=False)

    # img = serializers.ImageField()

    class Meta:
        model = Event
        fields = ['id', 'title', 'text', 'created_at', 'updated_at']


class CreateEventSerializer(serializers.ModelSerializer):
    title = serializers.CharField(max_length=128,
                                  allow_blank=False,
                                  required=True)
    text = serializers.CharField(allow_blank=True, required=False)
    due = serializers.DateTimeField(required=True)

    # img = serializers.ImageField()

    class Meta:
        model = Event
        fields = ['id', 'title', 'text', 'due', 'created_at', 'updated_at']
