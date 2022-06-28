from rest_framework import permissions

from pages import models


class BasePermissionPage(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True

    def has_object_permission(self, request, view, obj):
        match type(obj):
            case models.Page:
                return self._has_page_object_permission(request, view, obj)
            case models.Post:
                return self._has_post_object_permission(request, view, obj)
            case models.Tag:
                return self._has_tag_object_permission(request, view, obj)
            case models.Like:
                return self._has_like_object_permission(request, view, obj)
            case _:
                return False


class IsOwnerOrReadOnly(BasePermissionPage):
    @staticmethod
    def _has_page_object_permission(request, view, page: models.Page):
        return request.user == page.owner

    @staticmethod
    def _has_post_object_permission(request, view, post: models.Post):
        return request.user == post.page.owner

    @staticmethod
    def _has_tag_object_permission(request, view, tag: models.Tag):
        return False

    @staticmethod
    def _has_like_object_permission(request, view, like: models.Like):
        return request.user == like.owner


class IsNotBlockedPage(BasePermissionPage):
    @staticmethod
    def _has_page_object_permission(request, view, page: models.Page):
        return not page.owner.is_blocked

    @staticmethod
    def _has_post_object_permission(request, view, post: models.Post):
        return not post.page.owner.is_blocked

    @staticmethod
    def _has_tag_object_permission(request, view, tag: models.Tag):
        return False

    @staticmethod
    def _has_like_object_permission(request, view, like: models.Like):
        return not like.post.page.owner.is_blocked


class IsNotPrivatePage(BasePermissionPage):
    @staticmethod
    def _has_page_object_permission(request, view, page: models.Page):
        return not page.is_private

    @staticmethod
    def _has_post_object_permission(request, view, post: models.Post):
        return not post.page.is_private

    @staticmethod
    def _has_tag_object_permission(request, view, tag: models.Tag):
        return False

    @staticmethod
    def _has_like_object_permission(request, view, like: models.Like):
        return not like.post.page.is_private
