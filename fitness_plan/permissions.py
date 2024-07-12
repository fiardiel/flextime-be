from rest_framework import permissions
from fitness_plan.models import SessionTraining

class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user == request.user
    
class IsOwnerOfFitnessPlan(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.fitness_plan.user == request.user
    
class IsOwnerOfSessionPlan(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.session_plan.fitness_plan.user == request.user

class IsOwnerOfSessionTraining(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        customization_id = obj.id
        session_training = SessionTraining.objects.filter(customization=customization_id).first()
        return session_training.session_plan.fitness_plan.user == request.user