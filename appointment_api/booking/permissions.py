from rest_framework.permissions import BasePermission


class IsProvider(BasePermission):

    def has_permission(self, request, view):
        user = request.user
     #checks if current user exists, logged in and is a provider
        return bool(user and user.is_authenticated and getattr(user, 'is_provider', False))