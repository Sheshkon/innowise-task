from datetime import datetime

from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action, api_view
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST

from innotter.aws_services import upload_file_to_s3
from innotter.views import SerializersPermissionsBaseViewSet
from pages.filters import PageFilter
from users.permissions import IsAdmin, IsModerator, IsNotBlocked
from pages import permissions
from pages.models import Page, Tag, Post, Like

from pages.services import (
    block_page,
    create_like,
    create_post,
    add_follower,
    delete_follower,
    add_follow_request,
    delete_follow_request,
    accept_follow_request,
    reject_follow_request,
    add_tags_to_page,
    delete_tags_from_page,
)

from pages.serializers import (
    page_serializers,
    post_serializers,
    tag_serializers,
    like_serializer,
)


class PagesViewSet(SerializersPermissionsBaseViewSet):

    queryset = Page.objects.all()
    default_serializer_class = page_serializers.PageSerializer

    filter_backends = (DjangoFilterBackend,)
    search_fields = ('uuid', 'name', 'tags__name',)
    filterset_class = PageFilter

    serializer_classes_by_action = {
        'block': page_serializers.BlockPageSerializer,
        'create': page_serializers.CreatePageSerializer,
        'update': page_serializers.UpdatePageSerializer,
        'retrieve': page_serializers.RetrievePageSerializer,
        'list': page_serializers.ListPageSerializer,
        'list_follow_request': page_serializers.ListFollowRequestSerializer,
        'accept_followers': page_serializers.AcceptOrRejectRequestSerializer,
        'reject_followers': page_serializers.AcceptOrRejectRequestSerializer,
        'add_tags': page_serializers.TagsToPageSerializer,
        'delete_tags': page_serializers.TagsToPageSerializer,
    }

    permission_classes_by_action = {
        'create': (IsNotBlocked, permissions.IsOwnerOrReadOnly | IsAdmin | IsModerator,),
        'update': (IsNotBlocked, permissions.IsOwnerOrReadOnly | IsAdmin | IsModerator,),
        'partial_update': (IsNotBlocked, permissions.IsOwnerOrReadOnly | IsAdmin | IsModerator,),
        'retrieve': (AllowAny, permissions.IsNotPrivatePage, permissions.IsOwnerOrReadOnly | IsAdmin | IsModerator,),
        'list': (AllowAny,),
        'destroy': (IsNotBlocked, permissions.IsOwnerOrReadOnly | IsAdmin | IsModerator,),
        'follow': (IsNotBlocked,),
        'unfollow': (IsNotBlocked,),
        'send_follow_request': (IsNotBlocked,),
        'unsend_follow_request': (IsNotBlocked,),
        'accept_followers': (IsNotBlocked, permissions.IsOwnerOrReadOnly,),
        'reject_followers': (IsNotBlocked, permissions.IsOwnerOrReadOnly,),
        'list_follow_request': (IsNotBlocked, permissions.IsOwnerOrReadOnly,),
        'block': (IsAdmin | IsModerator,),
        'add_tags': (IsNotBlocked, permissions.IsOwnerOrReadOnly,),
        'delete_tags': (IsNotBlocked, permissions.IsOwnerOrReadOnly,),
    }

    @action(detail=True, methods=('patch',))
    def add_tags(self, request, pk=None):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        tags_names = serializer.validated_data.get('list_tag_names')
        page = self.get_object()
        add_tags_to_page(page=page, tags_names=tags_names)
        page_data = page_serializers.RetrievePageSerializer(page).data
        return Response(status=HTTP_200_OK, data=page_data)

    @action(detail=True, methods=('patch',))
    def delete_tags(self, request, pk=None):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        tags_names = serializer.validated_data.get('list_tag_names')
        page = self.get_object()
        delete_tags_from_page(page=page, tags_names=tags_names)
        page_data = page_serializers.RetrievePageSerializer(page).data
        return Response(status=HTTP_200_OK, data=page_data)

    @action(detail=True, methods=('patch',))
    def block(self, request, pk=None):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        page = block_page(page=self.get_object(), is_to_permanent=serializer.validated_data.get('is_to_permanent'))
        response_data = {
            'id': page.id,
            'unblock_date': page.unblock_date,
            'is_permanent_blocked': page.is_permanent_blocked
        }
        return Response(status=HTTP_200_OK, data=response_data)

    @action(detail=True, methods=('patch',))
    def follow(self, request, pk=None):
        if add_follower(page_to_follow=self.get_object(), follower=self.request.user):
            return Response(status=HTTP_200_OK)

        return Response(status=HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=('patch',))
    def unfollow(self, request, pk=None):
        if delete_follower(followed_page=self.get_object(), follower=self.request.user):
            return Response(status=HTTP_200_OK)

        return Response(status=HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=('patch',))
    def send_follow_request(self, request, pk=None):
        if add_follow_request(page_to_follow=self.get_object(), follower=self.request.user):
            return Response(status=HTTP_200_OK)

        return Response(status=HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=('patch',))
    def unsend_follow_request(self, request, pk=None):
        if delete_follow_request(followed_page=self.get_object(), follower=self.request.user):
            return Response(status=HTTP_200_OK)

        return Response(status=HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=('get',))
    def list_follow_request(self, request, pk=None):
        serializer = self.get_serializer(self.get_object())
        return Response(serializer.data)

    @action(detail=True, methods=('patch', ))
    def accept_followers(self, request, pk=None):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        one = serializer.validated_data['one']
        user_id = serializer.validated_data.get('user_id', None)
        accept_follow_request(page=self.get_object(), one=one, user_id=user_id)
        return Response(status=HTTP_200_OK)

    @action(detail=True, methods=('patch',))
    def reject_followers(self, request, pk=None):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        one = serializer.validated_data['one']
        user_id = serializer.validated_data.get('user_id', None)
        reject_follow_request(page=self.get_object(), one=one, user_id=user_id)
        return Response(status=HTTP_200_OK)

    def get_queryset(self   ):
        if self.action == 'list' and self.request.user.role == 'user':
            return Page.objects.filter(owner=self.request.user)

        return self.queryset

    def perform_update(self, serializer):
        image = self.request.FILES.get('file')
        if image:
            image_s3_path = upload_file_to_s3(
                file_path=image,
                key=f'{self.get_object().uuid}'
            )
            serializer.validated_data['image'] = image_s3_path
        serializer.save()


class TagsViewSet(SerializersPermissionsBaseViewSet):

    queryset = Tag.objects.all()
    default_serializer_class = tag_serializers.TagSerializer

    permission_classes_by_action = {
        'create': (IsNotBlocked,  IsAdmin | IsModerator,),
        'update': (IsNotBlocked, IsAdmin | IsModerator,),
        'partial_update': (IsNotBlocked, permissions.IsOwnerOrReadOnly | IsAdmin | IsModerator,),
        'retrieve': (permissions.IsOwnerOrReadOnly,),
        'list': (permissions.IsOwnerOrReadOnly,),
        'destroy': (IsNotBlocked, permissions.IsOwnerOrReadOnly | IsAdmin | IsModerator,),
    }


class PostsViewSet(SerializersPermissionsBaseViewSet):

    queryset = Post.objects.all()
    default_serializer_class = post_serializers.PostSerializer

    permission_classes_by_action = {
        'create': (IsNotBlocked, permissions.IsOwnerOrReadOnly | IsAdmin | IsModerator,),
        'update': (IsNotBlocked, permissions.IsOwnerOrReadOnly | IsAdmin | IsModerator,),
        'partial_update': (IsNotBlocked, permissions.IsOwnerOrReadOnly | IsAdmin | IsModerator,),
        'retrieve': (AllowAny,),
        'list': (AllowAny,),
        'destroy': (IsNotBlocked, permissions.IsOwnerOrReadOnly | IsAdmin | IsModerator,),
        'news': (IsNotBlocked, permissions.IsOwnerOrReadOnly)
    }

    serializer_classes_by_action = {
        'create': post_serializers.CreatePostSerializer,
        'update': post_serializers.UpdatePostSerializer,
        'list': post_serializers.RetrievePostSerializer,
        'retrieve': post_serializers.RetrievePostSerializer,
        'news': post_serializers.RetrievePostSerializer,
    }

    @action(detail=False, methods=('get',))
    def news(self, request):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def perform_create(self, serializer):
        create_post(user=self.request.user, serialized_post=serializer.validated_data)

    def get_queryset(self):
        if self.request.user.role == 'user':
            match self.action:
                case 'list':
                    return Post.objects.filter(page__owner=self.request.user)
                case 'news':
                    return Post.objects.filter(
                        Q(page__is_permanent_blocked=False) &
                        Q(page__owner__is_blocked=False) &
                        (Q(page__unblock_date__isnull=True) | Q(page__unblock_date__lt=datetime.now())) &
                        (Q(page__owner=self.request.user) | Q(page__followers__in=(self.request.user,)))
                    ).order_by('-updated_at', '-created_at')

        return self.queryset


class LikeViewSet(SerializersPermissionsBaseViewSet):

    queryset = Like.objects.all()
    default_serializer_class = like_serializer.LikeSerializer

    permission_classes_by_action = {
        'create': (IsNotBlocked,),
        'retrieve': (AllowAny,),
        'destroy': (IsNotBlocked, permissions.IsOwnerOrReadOnly | IsAdmin,),
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
        if self.action == 'list' and self.request.user.role == 'user':
            return Like.objects.filter(owner=self.request.user)

        return self.queryset
