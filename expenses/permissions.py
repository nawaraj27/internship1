from rest_framework import permissions

class IsOwnerOrSuperuser(permissions.BasePermission):
    """
    Custom permission to only allow owners or superusers to access/modify objects.
    """

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user or request.user.is_superuser
