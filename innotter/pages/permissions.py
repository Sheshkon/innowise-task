from rest_framework import permissions
from . import models


class IsOwnerOrReadOnly(permissions.BasePermission):

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
            case _:
                return False

    @staticmethod
    def _has_page_object_permission(request, view, page: models.Page):
        print(request.user, page.owner)
        return request.user == page.owner

    @staticmethod
    def _has_post_object_permission(request, view, post: models.Post):
        print(request.user == post.page.owner)
        return request.user == post.page.owner

    @staticmethod
    def _has_tag_object_permission(request, view, tag: models.Tag):
        return False


class IsNotPrivatePage(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True

    def has_object_permission(self, request, view, obj: models.Page):
        return not obj.is_private
