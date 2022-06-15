from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.decorators import api_view
from innotter.views import SerializersPermissionsViewSet

from .models import User
from . import serializers


@api_view()
def users_view(request):
    return Response({"message": "Users"})


class UserViewSet(SerializersPermissionsViewSet):
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
