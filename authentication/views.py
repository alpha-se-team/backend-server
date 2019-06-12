from rest_framework import status
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from drf_yasg.utils import swagger_auto_schema
import drf_yasg.openapi as openapi

from .renderers import UserJSONRenderer
from .serializers import (
    RegistrationSerializer,
    LoginSerializer,
    UserSerializer,
)


class RegistrationAPIView(APIView):
    permission_classes = (AllowAny, )
    renderer_classes = (UserJSONRenderer, )
    serializer_class = RegistrationSerializer

    # user_response = openapi.Response('reqeuse tdesc', RegistrationSerializer)

    @swagger_auto_schema(responses={200: serializer_class(many=True)})
    def post(self, request):
        user = request.data.get('user', {})
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class UserRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated, )
    renderer_classes = (UserJSONRenderer, )
    serializer_class = UserSerializer

    def retrieve(self, request, *args, **kargs):
        serializer = self.serializer_class(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        user_data = request.data.get('user', {})

        password = user_data.get('password')
        studentid = user_data.get('studentid')


        serializer_data = {
            'username' : user_data.get('username', request.user.username),

            # 'email' : user_data.get('email', request)
            # 'profile': {

            # }
        }
        if studentid is not None:
            serializer_data['student_id'] = studentid
        if password is not None:
            serializer_data['password'] = password

        serializer = self.serializer_class(request.user,
                                           data=serializer_data,
                                           partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class LoginAPIView(APIView):
    permission_classes = (AllowAny, )
    renderer_classes = (UserJSONRenderer, )
    serializer_class = LoginSerializer

    @swagger_auto_schema(responses={201: serializer_class})
    def post(self, request):
        user = request.data.get('user', {})
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
