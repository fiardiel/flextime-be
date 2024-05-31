from fitness_plan.models import FitnessPlan, Training, SessionPlan, Customization, SessionPlanTraining
from rest_framework import viewsets, response, status
from fitness_plan.serializers import FitnessPlanSerializer, TrainingSerializer, SessionPlanSerializer, CustomizationSerializer


class FitnessPlanViewSet(viewsets.ModelViewSet):
    queryset = FitnessPlan.objects.all()
    serializer_class = FitnessPlanSerializer

class SessionPlanViewSet(viewsets.ModelViewSet):
    queryset = SessionPlan.objects.all()
    serializer_class = SessionPlanSerializer

    def get_queryset(self):
        queryset = SessionPlan.objects.all()
        session_plan_id = self.request.query_params.get('session_plan_id', None)
        if session_plan_id is not None:
            queryset = queryset.filter(fitness_plan=session_plan_id)
        return queryset
    
    def destroy(self, request, *args, **kwargs):
        session_plan = self.get_object()
        session_plan.delete()
        return response.Response(status=status.HTTP_204_NO_CONTENT)


class TrainingViewSet(viewsets.ModelViewSet):
    queryset = Training.objects.all()
    serializer_class = TrainingSerializer

class CustomizationViewSet(viewsets.ModelViewSet):
    queryset = Customization.objects.all()
    serializer_class = CustomizationSerializer

class SessionTrainingViewSet(viewsets.ModelViewSet):
    queryset = SessionPlan.objects.all()
    serializer_class = SessionPlanSerializer

    def get_queryset(self):
        queryset = SessionPlanTraining.objects.all()
        session_plan_id = self.request.query_params.get('session_plan_id', None)
        if session_plan_id is not None:
            queryset = queryset.filter(session_plan=session_plan_id)
        return queryset
