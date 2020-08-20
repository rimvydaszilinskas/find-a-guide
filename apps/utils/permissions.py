from rest_framework.permissions import BasePermission


class ReadOnlyPermission(BasePermission):
    SAFE_METHODS = ['GET']

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return request.method in self.SAFE_METHODS
        return True
