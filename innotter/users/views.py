from django.utils.decorators import method_decorator
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_protect

from innotter.views import SerializersPermissionsBaseViewSet
from .models import User
from . import serializers
from .permissions import IsAdmin, IsModerator, IsNotAnonymous, IsNotBlocked
from .services import generate_refresh_token, generate_access_token, validate_user, check_user_refresh_token


class UsersViewSet(SerializersPermissionsBaseViewSet):
    queryset = User.objects.all()
    default_serializer_class = serializers.UserSerializer

    serializer_classes_by_action = {
        'create': serializers.CreateUserSerializer,
        'update': serializers.UpdateUserSerializer,
        'list': serializers.RetrieveUserSerializer,
        'retrieve': serializers.RetrieveUserSerializer,
        'register': serializers.RegistrationSerializer,
        'login_user': serializers.LoginSerializer,
    }

    permission_classes_by_action = {
        'create': (IsNotAnonymous, IsAdmin | IsModerator,),
        'update': (IsNotAnonymous, IsNotBlocked, IsAdmin | IsModerator,),
        'partial_update': (IsNotAnonymous, IsNotBlocked, IsAdmin | IsModerator,),
        'retrieve': (IsAuthenticated,),
        'list': (IsAuthenticated,),
        'destroy': (IsNotAnonymous, IsNotBlocked, IsAdmin | IsModerator,),
        'register': (AllowAny,),
        'login_user': (AllowAny,),
        'refresh_token': (AllowAny,),
    }

    @method_decorator(ensure_csrf_cookie)
    @action(detail=False, methods=('post',))
    def login_user(self, request):
        user = validate_user(request.data)
        serialized_user = self.get_serializer(user).data

        response = Response()
        response.set_cookie(key='refreshtoken', value=generate_refresh_token(user), httponly=True)
        response.data = {
            'access_token': generate_access_token(user),
            'user': serialized_user,
        }

        return response

    @action(detail=False, methods=('post',))
    @method_decorator(csrf_protect)
    def refresh_token(self, request):
        '''
        To obtain a new access_token this view expects 2 important things:
            1. a cookie that contains a valid refresh_token
            2. a header 'X-CSRFTOKEN' with a valid csrf token, client app can get it from cookies "csrftoken"
        '''
        user = check_user_refresh_token(request)
        access_token = generate_access_token(user)
        return Response({'access_token': access_token})

    @action(detail=False, methods=('post', ))
    def register(self, request):
        serializer = serializers.RegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)
