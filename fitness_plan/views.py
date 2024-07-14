from fitness_plan.models import FitnessPlan, Training, SessionPlan, Customization, SessionTraining
from rest_framework import viewsets, response, status, permissions
from fitness_plan.serializers import FitnessPlanSerializer, SessionPlanSerializer, CustomizationSerializer, SessionTrainingSerializer, TrainingSerializer
from rest_framework.response import Response
from django.db.models import F, Sum
from rest_framework.decorators import action
from fitness_plan.permissions import IsOwner, IsOwnerOfFitnessPlan, IsOwnerOfSessionPlan, IsOwnerOfSessionTraining, IsTrainingAdmin
from rest_framework.exceptions import PermissionDenied

class FitnessPlanViewSet(viewsets.ModelViewSet):
    queryset = FitnessPlan.objects.all()
    serializer_class = FitnessPlanSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]
    
    def perform_create(self, serializer):
        if 'user' in serializer.validated_data and serializer.validated_data['user'] != self.request.user:
            raise PermissionDenied("You don't have access for creating this fitness plan")
        serializer.save(user=self.request.user)

    @action(detail=False, methods=['GET'])
    def get_fitness_plan_by_user(self, request):
        user = request.user
        try:
            fitness_plan = FitnessPlan.objects.get(user=user)
            serialized_fitness_plan = FitnessPlanSerializer(fitness_plan).data
            return Response(serialized_fitness_plan)
        except FitnessPlan.DoesNotExist:
            return Response({'error': 'Fitness plan not found'}, status=status.HTTP_404_NOT_FOUND)

class SessionPlanViewSet(viewsets.ModelViewSet):
    queryset = SessionPlan.objects.all()
    serializer_class = SessionPlanSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOfFitnessPlan]
    
    def perform_create(self, serializer):
        fitness_plan = serializer.validated_data.get('fitness_plan', None)
        if fitness_plan and fitness_plan.user != self.request.user:
            raise PermissionDenied("You are unauthorized for this fitness plan")
        serializer.save()   

    @action(detail=True, methods=['get'])
    def total_duration(self, request, pk=None):
        session_plan = self.get_object()
        total_duration = session_plan.sessiontraining_set.annotate(
            total=F('customization__sets') * F('customization__reps') * F('customization__duration')
        ).aggregate(sum=Sum('total'))['sum']
        return response.Response({'total_duration': total_duration})

    def get_queryset(self):
        queryset = super().get_queryset()
        fitness_plan_id = self.request.GET.get('fitness_plan', None)
        if fitness_plan_id is not None:
            queryset = queryset.filter(fitness_plan=fitness_plan_id)
        return queryset
    
    def destroy(self, request, *args, **kwargs):
        session_plan = self.get_object()
        session_plan.delete()
        return response.Response(status=status.HTTP_204_NO_CONTENT)


class TrainingViewSet(viewsets.ModelViewSet):
    queryset = Training.objects.all()
    serializer_class = TrainingSerializer
    permission_classes = [permissions.IsAuthenticated, IsTrainingAdmin]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        training_type = self.request.GET.get('training_type', None)
        if training_type is not None:
            queryset = queryset.filter(training_type=training_type)
        return queryset

class CustomizationViewSet(viewsets.ModelViewSet):
    queryset = Customization.objects.all()
    serializer_class = CustomizationSerializer

    def get_permissions(self):
        if self.action in ['list', 'retreive', 'destroy', 'update', 'partial_update']:
            permission_classes = [permissions.IsAuthenticated, IsOwnerOfSessionTraining]
        else:
            permission_classes = [permissions.IsAuthenticated]

        return [permission() for permission in permission_classes]


class SessionTrainingViewSet(viewsets.ModelViewSet):
    queryset = SessionTraining.objects.all()
    serializer_class = SessionTrainingSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOfSessionPlan]

    def get_queryset(self):
        queryset = SessionTraining.objects.all()
        session_plan_id = self.request.GET.get('session_plan', None)
        if session_plan_id is not None:
            queryset = queryset.filter(session_plan=session_plan_id)
        return queryset
    
    @action(detail=False, methods=['get'])
    def count(self, request):
        queryset = self.get_queryset()
        count = queryset.count()
        return response.Response({'count': count})
