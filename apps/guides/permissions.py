from rest_framework.permissions import BasePermission


class PublicPreviewPrivateEditPermission(BasePermission):
    SAFE_METHODS = ['GET']

    def has_object_permission(self, request, view, obj):
        if request.method in self.SAFE_METHODS:
            return obj.active

        return obj.user == request.user

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return request.method in self.SAFE_METHODS
        return True
