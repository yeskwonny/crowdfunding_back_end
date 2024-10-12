from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # SAFE_METHODS like GET, HEAD, OPTIONS are allowed for any request
        if request.method in permissions.SAFE_METHODS:
            return True
        # If the user is admin or the owner, allow write access
        return obj.owner == request.user or request.user.is_staff

class IsSupporterOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.supporter == request.user or request.user.is_staff
    
class IsOnlyOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.username == request.user
