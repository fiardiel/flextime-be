from django.shortcuts import render
from fitness_plan.models import FitnessPlan, Training, SessionPlan, Customization
from rest_framework import viewsets, permissions
from fitness_plan.serializers import FitnessPlanSerializer, TrainingSerializer, SessionPlanSerializer, CustomizationSerializer


class FitnessPlanViewSet(viewsets.ModelViewSet):
    queryset = FitnessPlan.objects.all()
    serializer_class = FitnessPlanSerializer
    permission_classes = [permissions.IsAuthenticated]

class SessionPlanViewSet(viewsets.ModelViewSet):
    queryset = SessionPlan.objects.all()
    serializer_class = SessionPlanSerializer
    permission_classes = [permissions.IsAuthenticated]

class TrainingViewSet(viewsets.ModelViewSet):
    queryset = Training.objects.all()
    serializer_class = TrainingSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class CustomizationViewSet(viewsets.ModelViewSet):
    queryset = Customization.objects.all()
    serializer_class = CustomizationSerializer
    permission_classes = [permissions.IsAuthenticated]
