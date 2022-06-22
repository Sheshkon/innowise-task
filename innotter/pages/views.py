from rest_framework.permissions import AllowAny

from innotter.views import SerializersPermissionsBaseViewSet
from .models import Page, Tag, Post
from . import permissions
from users.permissions import IsAdmin, IsModerator, IsNotAnonymous, IsNotBlocked

from .serializers import (
    page_serializers,
    post_serializers,
    tag_serializers,
)


class PagesViewSet(SerializersPermissionsBaseViewSet):

    queryset = Page.objects.all()
    default_serializer_class = page_serializers.PageSerializer

    permission_classes_by_action = {
        'create': (IsNotAnonymous, IsNotBlocked, permissions.IsOwnerOrReadOnly | IsAdmin | IsModerator,),
        'update': (IsNotAnonymous, IsNotBlocked, permissions.IsOwnerOrReadOnly | IsAdmin | IsModerator,),
        'partial_update': (IsNotAnonymous, IsNotBlocked, permissions.IsOwnerOrReadOnly | IsAdmin | IsModerator,),
        'retrieve': (AllowAny, permissions.IsNotPrivatePage,),
        'list': (AllowAny, permissions.IsNotPrivatePage,),
        'destroy': (IsNotAnonymous, IsNotBlocked, permissions.IsOwnerOrReadOnly | IsAdmin | IsModerator,),
    }


class TagsViewSet(SerializersPermissionsBaseViewSet):

    queryset = Tag.objects.all()
    default_serializer_class = tag_serializers.TagSerializer

    permission_classes_by_action = {
        'create': (IsNotAnonymous, IsNotBlocked, permissions.IsOwnerOrReadOnly | IsAdmin | IsModerator,),
        'update': (IsNotAnonymous, IsNotBlocked, permissions.IsOwnerOrReadOnly | IsAdmin | IsModerator,),
        'partial_update': (IsNotAnonymous, IsNotBlocked, permissions.IsOwnerOrReadOnly | IsAdmin | IsModerator,),
        'retrieve': (AllowAny, permissions.IsNotPrivatePage),
        'list': (AllowAny, permissions.IsNotPrivatePage),
        'destroy': (IsNotAnonymous, IsNotBlocked, permissions.IsOwnerOrReadOnly | IsAdmin | IsModerator,),
    }


class PostsViewSet(SerializersPermissionsBaseViewSet):

    queryset = Post.objects.all()
    default_serializer_class = post_serializers.PostSerializer

    permission_classes_by_action = {
        'create': (IsNotAnonymous, IsNotBlocked, permissions.IsOwnerOrReadOnly | IsAdmin | IsModerator,),
        'update': (IsNotAnonymous, IsNotBlocked, permissions.IsOwnerOrReadOnly | IsAdmin | IsModerator,),
        'partial_update': (IsNotAnonymous, IsNotBlocked, permissions.IsOwnerOrReadOnly | IsAdmin | IsModerator,),
        'retrieve': (AllowAny,),
        'list': (AllowAny,),
        'destroy': (IsNotAnonymous, IsNotBlocked, permissions.IsOwnerOrReadOnly | IsAdmin | IsModerator,),
    }

    serializer_classes_by_action = {
        'create': post_serializers.CreatePostSerializer,
        'update': post_serializers.UpdatePostSerializer,
        'list': post_serializers.RetrievePostSerializer,
        'retrieve': post_serializers.RetrievePostSerializer,
    }


