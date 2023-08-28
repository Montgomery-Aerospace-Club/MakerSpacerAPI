from rest_framework import permissions


class AuthReadOnlyPermission(permissions.BasePermission):
    SAFE_METHODS = ("GET", "HEAD", "OPTIONS")

    def has_permission(self, request, view):
        # Allow read-only access for authenticated users
        if request.user and request.user.is_authenticated:
            if request.user.is_staff:  # Check if the user is an admin
                return True
            return view.action in ["list", "retrieve"]  # Allow read-only actions
        return False


class EveryoneReadOnlyPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        # Allow read-only access for authenticated users
        if request.user and request.user.is_authenticated:
            if request.user.is_staff:  # Check if the user is an admin
                return True
            return view.action in ["list", "retrieve"]  # Allow read-only actions
        return view.action in ["list", "retrieve"]


class AuthorizedUserCanOnlyReadAndUpdate(permissions.BasePermission):
    def has_permission(self, request, view):
        # Allow read-only access for authenticated users
        if request.user and request.user.is_authenticated:
            if request.user.is_staff:  # Check if the user is an admin
                return True
            return view.action != "destroy"  # Allow read-only actions
        return view.action in ["list", "retrieve"]
