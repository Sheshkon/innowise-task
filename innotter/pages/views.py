from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK

from innotter.views import SerializersPermissionsBaseViewSet
from .models import Page, Tag, Post, Like
from . import permissions
from users.permissions import IsAdmin, IsModerator, IsNotAnonymous, IsNotBlocked
from .services import block_page

from .serializers import (
    page_serializers,
    post_serializers,
    tag_serializers,
    like_serializer,
)


class PagesViewSet(SerializersPermissionsBaseViewSet):

    queryset = Page.objects.all()
    default_serializer_class = page_serializers.PageSerializer

    serializer_classes_by_action = {
        'block': page_serializers.BlockPageSerializer,
    }

    permission_classes_by_action = {
        'create': (IsNotAnonymous, IsNotBlocked, permissions.IsOwnerOrReadOnly | IsAdmin | IsModerator,),
        'update': (IsNotAnonymous, IsNotBlocked, permissions.IsOwnerOrReadOnly | IsAdmin | IsModerator,),
        'partial_update': (IsNotAnonymous, IsNotBlocked, permissions.IsOwnerOrReadOnly | IsAdmin | IsModerator,),
        'retrieve': (AllowAny, permissions.IsNotPrivatePage,),
        'list': (AllowAny, permissions.IsNotPrivatePage,),
        'destroy': (IsNotAnonymous, IsNotBlocked, permissions.IsOwnerOrReadOnly | IsAdmin | IsModerator,),
        'block': (IsAdmin | IsModerator,),
    }

    @action(detail=True, methods=('patch',))
    def block(self, request, pk=None):
        print('request.user', request.user)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        page = block_page(page=self.get_object(), is_to_permanent=serializer.validated_data.get('is_to_permanent'))
        response_data = {
            'id': page.id,
            'unblock_date': page.unblock_date,
        }
        return Response(status=HTTP_200_OK, data=response_data)


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


class LikeViewSet(SerializersPermissionsBaseViewSet):

    queryset = Like.objects.all()
    default_serializer_class = like_serializer.LikeSerializer

    permission_classes_by_action = {
        'create': (IsNotAnonymous, IsNotBlocked, permissions.IsOwnerOrReadOnly | IsAdmin | IsModerator,),
        'retrieve': (AllowAny,),
        'list': (AllowAny,),
        'destroy': (IsNotAnonymous, IsNotBlocked, permissions.IsOwnerOrReadOnly | IsAdmin | IsModerator,),
    }

    serializer_classes_by_action = {
        'create': post_serializers.CreatePostSerializer,
        'list': post_serializers.RetrievePostSerializer,
        'retrieve': post_serializers.RetrievePostSerializer,
    }
