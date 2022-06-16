from rest_framework.permissions import AllowAny

from innotter.views import SerializersPermissionsBaseViewSet
from .models import User
from . import serializers


class UserBaseViewSet(SerializersPermissionsBaseViewSet):
    queryset = User.objects.all()
    default_serializer_class = serializers.UserSerializer

    serializer_classes_by_action = {
        'create': serializers.CreateUserSerializer,
        'update': serializers.UpdateUserSerializer,
        'list': serializers.RetrieveUserSerializer,
        'retrieve': serializers.RetrieveUserSerializer,
    }

    permission_classes_by_action = {
        'create': (AllowAny,),
        'update': (AllowAny,),
        'partial_update': (AllowAny,),
        'retrieve': (AllowAny,),
        'list': (AllowAny,),
        'destroy': (AllowAny,),
    }
