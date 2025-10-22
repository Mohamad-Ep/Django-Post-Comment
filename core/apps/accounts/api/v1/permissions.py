from rest_framework import permissions
from rest_framework.permissions import BasePermission
# _______________________________________________________

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Object-level permission to only allow owners of an object to edit it.
    Assumes the model instance has an `owner` attribute.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Instance must have an attribute named `owner`.
        return obj.author.user == request.user

# _______________________________________________________

class IsAnonymousUser(BasePermission):
    """ just anonymous user access """

    def has_permission(self, request, view):
        return not request.user or request.user.is_anonymous
# _______________________________________________________