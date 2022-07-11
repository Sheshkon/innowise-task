from django.contrib.auth import get_user_model
from django.utils.decorators import method_decorator
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_protect
from rest_framework.status import HTTP_200_OK

from innotter.views import SerializersPermissionsBaseViewSet
from users import serializers
from users.permissions import IsAdmin, IsModerator, IsNotBlocked

from users.services import (
    generate_refresh_token,
    generate_access_token,
    validate_user,
    check_user_refresh_token,
    block_user,
)

User = get_user_model()


class UsersViewSet(SerializersPermissionsBaseViewSet):
    queryset = User.objects.all()
    default_serializer_class = serializers.UserSerializer

    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('username', 'first_name')
    search_fields = ('username', 'first_name',)

    serializer_classes_by_action = {
        'create': serializers.CreateUserSerializer,
        'update': serializers.UpdateUserSerializer,
        'partial_update': serializers.UpdateUserSerializer,
        'list': serializers.RetrieveUserSerializer,
        'retrieve': serializers.RetrieveUserSerializer,
        'register': serializers.RegistrationSerializer,
        'login_user': serializers.LoginSerializer,
    }

    permission_classes_by_action = {
        'create': (IsAdmin | IsModerator,),
        'update': (IsNotBlocked, IsAdmin | IsModerator,),
        'partial_update': (IsNotBlocked, IsAdmin | IsModerator,),
        'retrieve': (IsAuthenticated,),
        'list': (IsAuthenticated,),
        'destroy': (IsNotBlocked, IsAdmin,),
        'register': (AllowAny,),
        'login_user': (AllowAny,),
        'refresh_token': (AllowAny,),
        'block': (IsNotBlocked, IsAdmin,)
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

    @method_decorator(ensure_csrf_cookie)
    @action(detail=False, methods=('post', ))
    def register(self, request):
        serializer = serializers.RegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=('patch',))
    def block(self, request, pk=None):
        block_user(user=self.get_object())
        return Response(status=HTTP_200_OK)
