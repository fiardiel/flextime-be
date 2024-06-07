from fitness_plan.models import FitnessPlan, Training, SessionPlan, Customization, SessionTraining
from rest_framework import viewsets, response, status
from fitness_plan.serializers import FitnessPlanSerializer, SessionPlanSerializer, CustomizationSerializer, SessionTrainingSerializer, TrainingSerializer
from django.db.models import F, Sum
from rest_framework.decorators import action

class FitnessPlanViewSet(viewsets.ModelViewSet):
    queryset = FitnessPlan.objects.all()
    serializer_class = FitnessPlanSerializer

class SessionPlanViewSet(viewsets.ModelViewSet):
    queryset = SessionPlan.objects.all()
    serializer_class = SessionPlanSerializer

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
    
    def get_queryset(self):
        queryset = super().get_queryset()
        training_type = self.request.GET.get('training_type', None)
        if training_type is not None:
            queryset = queryset.filter(training_type=training_type)
        return queryset

class CustomizationViewSet(viewsets.ModelViewSet):
    queryset = Customization.objects.all()
    serializer_class = CustomizationSerializer

class SessionTrainingViewSet(viewsets.ModelViewSet):
    queryset = SessionTraining.objects.all()
    serializer_class = SessionTrainingSerializer

    def get_queryset(self):
        queryset = SessionTraining.objects.all()
        session_plan_id = self.request.GET.get('session_plan', None)
        if session_plan_id is not None:
            queryset = queryset.filter(session_plan=session_plan_id)
        return queryset
