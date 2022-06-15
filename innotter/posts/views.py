from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import generics, mixins, viewsets
from .models import Post

from .serializers import (
    PostSerializer,
    CreatePostSerializer,
    UpdatePostSerializer,
    RetrievePostSerializer,
)


@api_view()
def posts_view(request):
    return Response({"message": "Posts"})


class PostsViewSet(mixins.CreateModelMixin,
                   mixins.ListModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.DestroyModelMixin,
                   mixins.UpdateModelMixin,
                   viewsets.GenericViewSet):

    queryset = Post.objects.all()
    default_serializer_class = PostSerializer

    serializer_classes_by_action = {
        'create': CreatePostSerializer,
        'update': UpdatePostSerializer,
        'list': RetrievePostSerializer,
        'retrieve': RetrievePostSerializer,
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
