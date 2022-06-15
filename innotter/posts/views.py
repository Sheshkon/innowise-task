from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.response import Response
from rest_framework.decorators import api_view

from innotter.views import SerializersPermissionsViewSet
from .models import Post
from . import serializers


@api_view()
def posts_view(request):
    return Response({"message": "Posts"})


class PostsViewSet(SerializersPermissionsViewSet):

    queryset = Post.objects.all()
    default_serializer_class = serializers.PostSerializer

    serializer_classes_by_action = {
        'create': serializers.CreatePostSerializer,
        'update': serializers.UpdatePostSerializer,
        'list': serializers.RetrievePostSerializer,
        'retrieve': serializers.RetrievePostSerializer,
    }

    permission_classes_by_action = {
        'create': (AllowAny,),
        'update': (AllowAny,),
        'partial_update': (AllowAny,),
        'retrieve': (AllowAny,),
        'list': (AllowAny,),
        'destroy': (AllowAny,),
    }
