from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """Allow unsafe methods only for the object owner."""

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return getattr(obj, "user", None) == request.user
