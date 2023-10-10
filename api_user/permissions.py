from rest_framework import permissions


class IsOwnerOrSuperUser(permissions.BasePermission):
    # ログインユーザー本人のみ
    def has_object_permission(self, request, view, obj):
        return bool(request.user == obj or request.user.is_superuser)


class IsSuperUser(permissions.BasePermission):
    # SuperUserのみ
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_superuser)
