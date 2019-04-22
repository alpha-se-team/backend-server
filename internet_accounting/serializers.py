from django.contrib.auth.models import User
from rest_framework import serializers
from .models import UserProfile


        # user = User.objects.create_user(
        #     username=validated_data['username'],
        #     password=validated_data['password'],
        #     first_name=validated_data['first_name'],
        #     last_name=validated_data['last_name'],
        #     email=validated_data['email'],
        #     # is_staff=validated_data['is_staff'],
        #     # is_superuser=validated_data['is_superuser']
        # )
class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        '''
        create user
        '''
        password = validated_data.pop('password')
        user = User.objects.create(**validated_data)
        print("help")
        print(type(user))
        print(user)
        user.set_password(password)
        return user

    def update(self, instance, validated_data):
        '''
        update user only
        '''
        instance.username = validated_data.get('username', instance.username)
        instance.set_password(validated_data.get('password', instance.password))
        instance.email = validated_data.get('email', instance.email)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.is_staff = validated_data.get('is_staff', instance.is_staff)
        instance.save()
        return instance

    class Meta:
        model = User
        fields = '__all__'


class TokenSerializer(serializers.Serializer):
    '''
    for jwt token
    '''
    token = serializers.CharField(max_length=255)


class UserProfileSerializer(serializers.ModelSerializer):
    '''
    A serializer which sits on top of UserPofile model.
    '''
    user = UserSerializer(required=True)

    def create(self, validated_data):
        '''
        create profile + user
        '''
        user_data = validated_data.pop('user')
        user = UserSerializer.create(UserSerializer(), validated_data=user_data)
        profile, created = UserProfile.objects.update_or_create(user=user, **validated_data)
        return profile

    # def update(self, instance, validated_data):
    #     '''
    #     update profile + user
    #     '''
    #     user_data = validated_data.pop('user')
    #     self.user(instance.user, user_data)

    #     instance.total_bandwidth = validated_data.get('total_bandwidth', instance.total_bandwidth)
    #     instance.save()
    #     return instance

    class Meta:
        model = UserProfile
        fields = '__all__'
