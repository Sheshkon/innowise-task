from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK

from innotter.views import SerializersPermissionsBaseViewSet
from .models import Page, Tag, Post, Like
from . import permissions
from users.permissions import IsAdmin, IsModerator, IsNotAnonymous, IsNotBlocked
from .services import (
    block_page,
    create_like,
    create_post,
)

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
        'create': page_serializers.CreatePageSerializer,
        'update': page_serializers.UpdatePageSerializer,
        'retrieve': page_serializers.RetrievePageSerializer,
        'list': page_serializers.ListPageSerializer,
    }

    permission_classes_by_action = {
        'create': (IsNotAnonymous, IsNotBlocked, permissions.IsOwnerOrReadOnly | IsAdmin | IsModerator,),
        'update': (IsNotAnonymous, IsNotBlocked, permissions.IsOwnerOrReadOnly | IsAdmin | IsModerator,),
        'partial_update': (IsNotAnonymous, IsNotBlocked, permissions.IsOwnerOrReadOnly | IsAdmin | IsModerator,),
        'retrieve': (AllowAny, permissions.IsNotPrivatePage, permissions.IsOwnerOrReadOnly),
        'list': (AllowAny,),
        'destroy': (IsNotAnonymous, IsNotBlocked, permissions.IsOwnerOrReadOnly | IsAdmin | IsModerator,),
        'block': (IsAdmin | IsModerator,),
    }

    @action(detail=True, methods=('patch',))
    def add_tags(self, request, pk=None):
        pass

    @action(detail=True, methods=('patch',))
    def delete_tags(self, request, pk=None):
        pass

    @action(detail=True, methods=('patch',))
    def block(self, request, pk=None):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        page = block_page(page=self.get_object(), is_to_permanent=serializer.validated_data.get('is_to_permanent'))
        response_data = {
            'id': page.id,
            'unblock_date': page.unblock_date,
        }
        return Response(status=HTTP_200_OK, data=response_data)

    def get_queryset(self):
        if self.action == 'list' and self.requset.user == 'user':
            return Page.objects.filter(owner=self.request.user)

        return self.queryset


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

    def perform_create(self, serializer):
        create_post(user=self.request.user, serialized_post=serializer.validated_data)

    def get_queryset(self):
        if self.action == 'list' and self.requset.user == 'user':
            return Post.objects.filter(page__owner=self.request.user)

        return self.queryset


class LikeViewSet(SerializersPermissionsBaseViewSet):

    queryset = Like.objects.all()
    default_serializer_class = like_serializer.LikeSerializer

    permission_classes_by_action = {
        'create': (IsNotAnonymous, IsNotBlocked, IsAdmin | IsModerator,),
        'retrieve': (AllowAny,),
        'destroy': (IsNotAnonymous, IsNotBlocked, permissions.IsOwnerOrReadOnly | IsAdmin | IsModerator,),
        'list': (AllowAny,),
    }

    serializer_classes_by_action = {
        'create': like_serializer.CreateLikeSerializer,
        'list': like_serializer.RetrieveLikeSerializer,
        'retrieve': like_serializer.RetrieveLikeSerializer,
    }

    def perform_create(self, serializer):
        create_like(user=self.request.user, post=serializer.validated_data.get('post'))

    def get_queryset(self):
        if self.action == 'list' and self.requset.user == 'user':
            return Like.objects.filter(owner=self.request.user)

        return self.queryset
