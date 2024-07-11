from datetime import datetime
from django.contrib.auth.models import User, Group
from rest_framework.decorators import action
from course_plan.models import ClassSchedule
from fitness_plan.models import SessionPlan
from fitness_plan.serializers import SessionPlanSerializer
from main.models import SessionSchedule, ActivityPlan
from course_plan.models import AssignmentDeadline, ClassSchedule, TestSchedule
from rest_framework import viewsets, permissions, response, status
from main.serializers import UserSerializer, GroupSerializer, SessionScheduleSerializer, ActivityPlanSerializer
from course_plan.serializers import AssignmentDeadlineSerializer, ClassScheduleSerializer, TestScheduleSerializer

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

    @action(detail=True, methods=['get'])
    def get_available_session_plans(self, request, pk=None):
        activity_plan = self.get_object()
        session_plans = SessionPlan.objects.filter(fitness_plan=activity_plan.fitness_plan).exclude(id__in=activity_plan.sessionschedule_set.all().values_list('session_plan', flat=True))
        serialized_session_plans = SessionPlanSerializer(session_plans, many=True).data
        return response.Response(serialized_session_plans)

    @action(detail=True, methods=['get'])
    def get_schedules(self, request, pk=None):
        try:
            activity_plan = self.get_object()
            unformatted_date = request.query_params.get('date')
            date = datetime.strptime(unformatted_date, '%Y%m%d').strftime('%Y-%m-%d')
            day = datetime.strptime(date, '%Y-%m-%d').weekday() + 1
            day_map = {1: "MON", 2: "TUE", 3: "WED", 4: "THU", 5: "FRI", 6: "SAT", 7: "SUN"}

            session_schedules = SessionSchedule.objects.filter(activity_plan=activity_plan, day=day_map[day]).select_related('session_plan')
            class_schedules = ClassSchedule.objects.filter(course_plan=activity_plan.course_plan, class_day=day_map[day])
            test_schedules = TestSchedule.objects.filter(course_plan=activity_plan.course_plan, test_date=date)
            assignment_deadlines = AssignmentDeadline.objects.filter(course_plan=activity_plan.course_plan, assignment_due_date=date)

            serialized_session_schedules = SessionScheduleSerializer(session_schedules, many=True).data
            serialized_class_schedules = ClassScheduleSerializer(class_schedules, many=True).data
            serialized_test_schedules = TestScheduleSerializer(test_schedules, many=True).data
            serialized_assignment_deadlines = AssignmentDeadlineSerializer(assignment_deadlines, many=True).data

            return response.Response({
                'session_schedules': serialized_session_schedules,
                'class_schedules': serialized_class_schedules,
                'test_schedules': serialized_test_schedules,
                'assignment_deadlines': serialized_assignment_deadlines
            })
        except ActivityPlan.DoesNotExist:
            return response.Response({'message': 'Activity plan does not exist'}, status=status.HTTP_400_BAD_REQUEST)


class SessionScheduleViewSet(viewsets.ModelViewSet):
    queryset = SessionSchedule.objects.all().order_by('day', 'start_time')
    serializer_class = SessionScheduleSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        activity_plan_id = self.request.GET.get("activity_plan", None)
        if activity_plan_id is not None:
            queryset = queryset.filter(activity_plan=activity_plan_id)  
        return queryset

    def create(self, request, *args, **kwargs):
        start_time = request.data.get('start_time')
        end_time = request.data.get('end_time')
        day = request.data.get('day')
        activity_plan_id = request.data.get('activity_plan')
        activity_plan = ActivityPlan.objects.get(id=activity_plan_id)

        if end_time <= start_time:
            return response.Response({'message': 'End time must be after start time'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            activity_plan = ActivityPlan.objects.get(id=activity_plan_id)
            course_plan= activity_plan.course_plan
        except ActivityPlan.DoesNotExist:
            return response.Response({'message': 'Activity plan does not exist'}, status=status.HTTP_400_BAD_REQUEST)

        class_schedules = ClassSchedule.objects.filter(course_plan=course_plan)

        overlapping_classes = class_schedules.filter(
            start_time__lt=end_time,
            end_time__gt=start_time,
            class_day=day,
            course_plan=course_plan
        )

        overlapping_schedules = SessionSchedule.objects.filter(
            start_time__lt=end_time,
            end_time__gt=start_time,
            day=day,
            session_plan__fitness_plan=activity_plan.fitness_plan
        )

        if overlapping_schedules.exists() or overlapping_classes.exists():
            return response.Response({'message': 'Schedule overlaps with existing schedule'}, status=status.HTTP_400_BAD_REQUEST)
        
        return super().create(request, *args, **kwargs)
    
    def update(self, request, *args, **kwargs):
        start_time = request.data.get('start_time')
        end_time = request.data.get('end_time')
        day = request.data.get('day')
        activity_plan_id = request.data.get('activity_plan')
        session_schedule_id = self.get_object().id

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
        ).exclude(id=session_schedule_id)

        if overlapping_schedules.exists() or overlapping_classes.exists():
            return response.Response({'message': 'Schedule overlaps with existing schedule'}, status=status.HTTP_400_BAD_REQUEST)
        
        return super().update(request, *args, **kwargs)
