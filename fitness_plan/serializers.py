from django.contrib.auth.models import User
from rest_framework import serializers
from fitness_plan.models import FitnessPlan, Training, SessionPlan, Customization


class FitnessPlanSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = FitnessPlan
        fields = '__all__'

class SessionPlanSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = SessionPlan
        fields = '__all__'

class TrainingSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Training
        fields = '__all__'

class CustomizationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Customization
        fields = '__all__'

