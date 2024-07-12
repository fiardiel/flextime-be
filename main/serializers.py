from rest_framework import serializers
from django.contrib.auth.models import Group
from users.models import User
from main.models import ActivityPlan, SessionSchedule
class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']


class ActivityPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActivityPlan
        fields = '__all__'


class SessionScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = SessionSchedule
        fields = '__all__'