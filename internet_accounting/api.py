from rest_framework import generics, permissions, status
# from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_jwt.settings import api_settings

from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login

from .models import UserProfile
from .serializers import UserSerializer, UserProfileSerializer, TokenSerializer


jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER


# class HelloView(APIView):

#     def get(self, reqeust):
#         content = {'message': 'Hello World'}
#         print(type(reqeust))
#         return Response(content)


# class BaseManageView(APIView):
#     """
#     The base class for ManageViews
#         A ManageView is a view which is used to dispatch the requests to the appropriate views
#         This is done so that we can use one URL with different methods (GET, PUT, etc)
#     """
#     def dispatch(self, request, *args, **kwargs):
#         if not hasattr(self, 'VIEWS_BY_METHOD'):
#             raise Exception('VIEWS_BY_METHOD static dictionary variable must be defined on a ManageView class!')
#         if request.method in self.VIEWS_BY_METHOD:
#             return self.VIEWS_BY_METHOD[request.method]()(request, *args, **kwargs)

#         return Response(status=405)



class ListUsersProfiles(generics.ListAPIView):
    """
    show all users
    GET user/all
    """
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer


class UserLoginView(generics.CreateAPIView):
    """
    POST auth/login
    """
    permission_classes = (permissions.AllowAny, )  # Override global permission
    queryset = User.objects.all()
    authentication_classes = (JSONWebTokenAuthentication, )

    def post(self, request, *args, **kargs):
        username = request.data.get("username", "")
        password = request.data.get("password", "")
        print(username, password)
        user = authenticate(request, username=username, password=password)
        if user is not None:
            # Save user's ID in the session using DRF
            login(request, user)
            serializer = TokenSerializer(data={
                "token": jwt_encode_handler(
                    jwt_payload_handler(user)
                )})
            serializer.is_valid()
            return Response(serializer.data)
        return Response(status=status.HTTP_401_UNAUTHORIZED)


class UserProfileInfoView(generics.RetrieveAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = (permissions.IsAuthenticated,)
    queryset = UserProfile.objects.all()
    authentication_classes = (JSONWebTokenAuthentication, )


class RegisterUserProfileView(generics.CreateAPIView):
    """
    POST auth/register
    """
    serializer_class = UserProfileSerializer
    permission_classes = (permissions.AllowAny,)
    queryset = UserProfile.objects.all()

    # def post(self, reqeust, *args, **kargs):
    #     bad_info_response = Response(
    #         data={
    #             'message': 'bad info'
    #         },
    #         status=status.HTTP_400_BAD_REQUEST)

    #     def get_value(key):
    #         return reqeust.data.get(key, '')

        # username = get_value('username')
        # password = get_value('password')
        # email = get_value('email')
        # is_staff = bool(get_value('is_staff'))
        # print(username, password, email, is_staff)
        # if '' in [username, password, email]:
        #     return bad_info_response
        # User.objects.create_user(
        #     username=username, password=password, email=email,
        #     is_staff=is_staff)

        # return Response(status=status.HTTP_201_CREATED)


# class GetUserView(generics.CreateAPIView):
#     """
#     GET user/<int:pk>
#     """
#     def get(self, request, format=None) -> Response:
#          return None

# class UserProfileView(BaseManageView):
#     VIEWS_BY_METHOD = {
#         # 'DELETE': .as_view,
#         'GET': ProductDetailsView.as_view,
#         # 'PUT': ProductUpdateView.as_view,
#         # 'PATCH': ProductUpdateView.as_view
#         'POST': RegisterUserProfileView.as_view,
#     }
