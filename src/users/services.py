# permissions input
from rest_framework import permissions




# permission clases
class AdminOnlyPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_superuser:
            return True