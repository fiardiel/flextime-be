from rest_framework import permissions

class IsOwnerOrAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user or request.user.is_staff or request.user.is_superuser
    def has_permission(self, request, view):
        return request.user.is_authenticated
    
class IsCoursePlanOwnerOrAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.course_plan.user == request.user or request.user.is_staff or request.user.is_superuser
    def has_permission(self, request, view):
        return request.user.is_authenticated