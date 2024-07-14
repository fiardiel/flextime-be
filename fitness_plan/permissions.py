from rest_framework import permissions
from fitness_plan.models import SessionTraining


class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user or request.user.is_staff or request.user.is_superuser
    
class IsOwnerOfFitnessPlan(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.fitness_plan.user == request.user or request.user.is_staff or request.user.is_superuser
    
class IsOwnerOfSessionPlan(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.session_plan.fitness_plan.user == request.user or request.user.is_staff or request.user.is_superuser

class IsOwnerOfSessionTraining(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        customization_id = obj.id
        session_training = SessionTraining.objects.filter(customization=customization_id).first()
        return session_training.session_plan.fitness_plan.user == request.user or request.user.is_staff or request.user.is_superuser
    
class IsTrainingAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_staff or request.user.is_superuser