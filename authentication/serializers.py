from django.contrib.auth import authenticate

from rest_framework import serializers

from account.serializers import ProfileSerializer
from .models import User
from core.fields import Base64Field


class RegistrationSerializer(serializers.ModelSerializer):
    """Serializers registration requests and creates a new user."""

    password = serializers.CharField(
        max_length=128,
        min_length=4,
        write_only=True
    )
    token = serializers.CharField(max_length=255, read_only=True)

    class Meta:
        model = User
        # fields = '__all__'#a ['email', 'username', 'password', 'token']
        exclude = ('img', )

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance


class LoginSerializer(serializers.Serializer):
    # email = serializers.CharField(max_length=255)
    username = serializers.CharField(max_length=255)#, read_only=True)
    password = serializers.CharField(max_length=128, write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)

    # class Meta:
    #     model = User
    #     fields = '__all__'
    #     read_only_fields = ('token',)

    def validate(self, data):
        username = data.get('username', None)
        password = data.get('password', None)
        if username is None:
            raise serializers.ValidationError(
                'A username is required to log in.'
            )
        if password is None:
            raise serializers.ValidationError(
                'A password is required to log in.'
            )
        user = authenticate(username=username, password=password)
        if user is None:
            raise serializers.ValidationError(
                'A user with this username and password was not found'
            )
        if not user.is_active:
            raise serializers.ValidationError(
                'This user has been deactivated.'
            )
        return {
            'email': user.email,
            'username': user.username,
            'token': user.token,
        }


class ImageUserSerializer(serializers.ModelSerializer):
    img = Base64Field()  # Hackty hack hack
    # img = serializers.ImageField()

    class Meta:
        model = User
        fields = [
            'img',
        ]


class UserSerializer(serializers.ModelSerializer):
    """Handles serialization and deserialization of User objects."""

    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True
    )

    profile = ProfileSerializer(write_only=True)


    class Meta:
        model = User
        # fields = '__all__'
        exclude = ('img', )
        read_only_fields = ('token',)

    def update(self, instance, validated_data):
        """Performs an update on a User."""
        password = validated_data.pop('password', None)
        profile_data = validated_data.pop('profile', {})

        if password is not None:
            instance.set_password(password)

        for (key, value) in validated_data.items():
            setattr(instance, key, value)
        instance.save()

        # let's update profile
        for (k, v) in profile_data.items():
            setattr(instance.profile, k, v)

        instance.profile.save()
        return instance
