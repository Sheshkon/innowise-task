from rest_framework import permissions


class IsNotAnonymous(permissions.BasePermission):

    def has_permission(self, request, view):
        return not request.user.is_anonymous


class IsAdmin(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user.is_staff or request.user.role == request.user.Roles.ADMIN.value


class IsModerator(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user.role == request.user.Roles.MODERATOR.value


class IsUser(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user.role == request.user.Roles.MODERATOR


class IsNotBlocked(permissions.BasePermission):
    def has_permission(self, request, view):
        return not request.user.is_blocked
