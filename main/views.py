from django.contrib.auth.models import User, Group
from main.models import SessionSchedule, ActivityPlan
from rest_framework import viewsets
from rest_framework import permissions
from main.serializers import UserSerializer, GroupSerializer, SessionScheduleSerializer, ActivityPlanSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]

class ActivityPlanViewSet(viewsets.ModelViewSet):
    queryset = ActivityPlan.objects.all()
    serializer_class = ActivityPlanSerializer

class SessionScheduleViewSet(viewsets.ModelViewSet):
    queryset = SessionSchedule.objects.all()
    serializer_class = SessionScheduleSerializer