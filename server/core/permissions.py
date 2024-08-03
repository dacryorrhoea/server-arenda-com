from rest_framework import permissions


class IsOwnerOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return True

    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True

        return obj.owner == request.user
    
class IsLessorOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.groups.filter(name="Lessor").exists():
            return True
        return False
    
class IsRentorOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.groups.filter(name="Rentor").exists():
            return True
        return False

