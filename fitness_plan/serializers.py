from rest_framework import serializers
from fitness_plan.models import FitnessPlan, Training, SessionPlan, Customization, SessionTraining


class FitnessPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = FitnessPlan
        fields = '__all__'

class SessionPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = SessionPlan
        fields = '__all__'

class TrainingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Training
        fields = '__all__'

class CustomizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customization
        fields = '__all__'

class SessionTrainingSerializer(serializers.ModelSerializer):
    class Meta:
        model = SessionTraining
        fields = '__all__'
