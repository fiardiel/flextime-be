from django.contrib.auth.models import User, Group
from course_plan.models import ClassSchedule
from main.models import SessionSchedule, ActivityPlan
from rest_framework import viewsets, permissions, response, status
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
    queryset = SessionSchedule.objects.all().order_by('day', 'start_time')
    serializer_class = SessionScheduleSerializer

    def create(self, request, *args, **kwargs):
        start_time = request.data.get('start_time')
        end_time = request.data.get('end_time')
        day = request.data.get('day')
        activity_plan_id = request.data.get('activity_plan')

        if end_time <= start_time:
            return response.Response({'message': 'End time must be after start time'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            activity_plan = ActivityPlan.objects.get(id=activity_plan_id)
            course_plan_id = activity_plan.course_plan
        except ActivityPlan.DoesNotExist:
            return response.Response({'message': 'Activity plan does not exist'}, status=status.HTTP_400_BAD_REQUEST)

        class_schedules = ClassSchedule.objects.filter(course_plan=course_plan_id)

        overlapping_classes = class_schedules.filter(
            start_time__lt=end_time,
            end_time__gt=start_time,
            class_day=day
        )

        overlapping_schedules = SessionSchedule.objects.filter(
            start_time__lt=end_time,
            end_time__gt=start_time,
            day=day
        )

        if overlapping_schedules.exists() or overlapping_classes.exists():
            return response.Response({'message': 'Schedule overlaps with existing schedule'}, status=status.HTTP_400_BAD_REQUEST)
        

        
        return super().create(request, *args, **kwargs)