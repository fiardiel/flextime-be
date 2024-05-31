from django.shortcuts import render
from fitness_plan.models import FitnessPlan, Training, SessionPlan, Customization
from rest_framework import viewsets, permissions
from fitness_plan.serializers import FitnessPlanSerializer, TrainingSerializer, SessionPlanSerializer, CustomizationSerializer


class FitnessPlanViewSet(viewsets.ModelViewSet):
    queryset = FitnessPlan.objects.all()
    serializer_class = FitnessPlanSerializer

class SessionPlanViewSet(viewsets.ModelViewSet):
    queryset = SessionPlan.objects.all()
    serializer_class = SessionPlanSerializer

    def get_queryset(self):
        queryset = SessionPlan.objects.all()
        fitness_plan_id = self.request.query_params.get('fitness_plan_id', None)
        if fitness_plan_id is not None:
            queryset = queryset.filter(fitness_plan=fitness_plan_id)
        return queryset

class TrainingViewSet(viewsets.ModelViewSet):
    queryset = Training.objects.all()
    serializer_class = TrainingSerializer

class CustomizationViewSet(viewsets.ModelViewSet):
    queryset = Customization.objects.all()
    serializer_class = CustomizationSerializer

