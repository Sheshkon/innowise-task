from rest_framework import mixins, viewsets
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.decorators import api_view

from .models import User
from .serializers import (
    UserSerializer,
    CreateUserSerializer,
    UpdateUserSerializer,
    UpdateUserInfoSerializer,
    RetrieveUserSerializer,

)


@api_view()
def users_view(request):
    return Response({"message": "Users"})


class UserViewSet(mixins.CreateModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.DestroyModelMixin,
                  mixins.ListModelMixin,
                  viewsets.GenericViewSet):
    queryset = User.objects.all()
    default_serializer_class = UserSerializer

    serializer_classes_by_action = {
        'create': CreateUserSerializer,
        'update': UpdateUserSerializer,
        'list': RetrieveUserSerializer,
        'retrieve': RetrieveUserSerializer,
    }

    permission_classes_by_action = {
        'create': (AllowAny,),
        'update': (AllowAny,),
        'partial_update': (AllowAny,),
        'retrieve': (AllowAny,),
        'list': (AllowAny,),
        'destroy': (AllowAny,),
    }

    def get_serializer_class(self):
        return self.serializer_classes_by_action.get(self.action, self.default_serializer_class)

    def get_permissions(self):
        try:
            # return permission_classes depending on `action`
            return [permission() for permission in self.permission_classes_by_action[self.action]]
        except KeyError:
            # action is not set return default permission_classes
            return [permission() for permission in self.permission_classes]
