from rest_framework.permissions import AllowAny

from innotter.views import SerializersPermissionsBaseViewSet
from .models import Page, Tag, Post
from .serializers import (
    page_serializers,
    post_serializers,
    tag_serializers,
)


class PagesBaseViewSet(SerializersPermissionsBaseViewSet):

    queryset = Page.objects.all()
    default_serializer_class = page_serializers.PageSerializer

    serializer_classes_by_action = {
        'create': page_serializers.PageSerializer,
        'update': page_serializers.PageSerializer,
        'list': page_serializers.PageSerializer,
        'retrieve': page_serializers.PageSerializer,
    }

    permission_classes_by_action = {
        'create': (AllowAny,),
        'update': (AllowAny,),
        'partial_update': (AllowAny,),
        'retrieve': (AllowAny,),
        'list': (AllowAny,),
        'destroy': (AllowAny,),
    }


class TagsBaseViewSet(SerializersPermissionsBaseViewSet):

    queryset = Tag.objects.all()
    default_serializer_class = tag_serializers.TagSerializer

    permission_classes_by_action = {
        'create': (AllowAny,),
        'update': (AllowAny,),
        'partial_update': (AllowAny,),
        'retrieve': (AllowAny,),
        'list': (AllowAny,),
        'destroy': (AllowAny,),
    }


class PostsBaseViewSet(SerializersPermissionsBaseViewSet):

    queryset = Post.objects.all()
    default_serializer_class = post_serializers.PostSerializer

    serializer_classes_by_action = {
        'create': post_serializers.CreatePostSerializer,
        'update': post_serializers.UpdatePostSerializer,
        'list': post_serializers.RetrievePostSerializer,
        'retrieve': post_serializers.RetrievePostSerializer,
    }

    permission_classes_by_action = {
        'create': (AllowAny,),
        'update': (AllowAny,),
        'partial_update': (AllowAny,),
        'retrieve': (AllowAny,),
        'list': (AllowAny,),
        'destroy': (AllowAny,),
    }
