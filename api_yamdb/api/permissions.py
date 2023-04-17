from rest_framework import permissions

MODERATOR_METHODS = ('PATCH', 'DELETE')


class IsAdminOrSuperUser(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return (
                request.user.role == 'admin'
                or request.user.is_superuser
            )


class AdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
            and request.user.role == 'admin'
        )


class IsAuthorOrReadOnlyPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or obj.author == request.user
            or (request.method in MODERATOR_METHODS
                and request.user.role == 'moderator')
            or request.user.role == 'admin'
        )


class IsAdminOrReadOnlyPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.role == 'adm'
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.role == 'adm'
        )
