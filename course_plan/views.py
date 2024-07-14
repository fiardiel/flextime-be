from course_plan.models import AssignmentDeadline, ClassSchedule, TestSchedule, CoursePlan
from rest_framework import viewsets, response, status, permissions
from course_plan.serializers import AssignmentDeadlineSerializer, ClassScheduleSerializer, TestScheduleSerializer, CoursePlanSerializer
from course_plan.permissions import IsOwnerOrAdmin, IsCoursePlanOwnerOrAdmin

class CoursePlanViewSet(viewsets.ModelViewSet):
    queryset = CoursePlan.objects.all()
    serializer_class = CoursePlanSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrAdmin]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff or user.is_superuser:
            return CoursePlan.objects.all()
        return CoursePlan.objects.filter(user=user)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        response_dict = {
            'course_plan': self.get_serializer(instance).data,
            'class_schedules': ClassScheduleSerializer(instance.classschedule_set.all(), many=True).data,
            'test_schedules': TestScheduleSerializer(instance.testschedule_set.all(), many=True).data,
            'assignment_deadlines': AssignmentDeadlineSerializer(instance.assignmentdeadline_set.all(), many=True).data,
        }
        return response.Response(response_dict)
    

class ClassScheduleViewSet(viewsets.ModelViewSet):
    queryset = ClassSchedule.objects.all().order_by('class_day', 'start_time')
    serializer_class = ClassScheduleSerializer
    permission_classes = [permissions.IsAuthenticated, IsCoursePlanOwnerOrAdmin]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff or user.is_superuser:
            return ClassSchedule.objects.all().order_by('class_day', 'start_time')
        return ClassSchedule.objects.filter(course_plan__user=user).order_by('class_day', 'start_time')

    def create(self, request, *args, **kwargs):
        user = request.user
        try:
            course_plan = CoursePlan.objects.get(user=user)
        except CoursePlan.DoesNotExist:
            return response.Response({'message': 'Course plan does not exist'}, status=status.HTTP_400_BAD_REQUEST)

        start_time = request.data.get('start_time')
        end_time = request.data.get('end_time')
        day = request.data.get('class_day')

        if end_time <= start_time:
            return response.Response({'message': 'End time must be after start time'}, status=status.HTTP_400_BAD_REQUEST)
        
        overlapping_schedules = ClassSchedule.objects.filter(
            start_time__lt=end_time,
            end_time__gt=start_time,
            class_day=day,
            course_plan=course_plan
        )

        if overlapping_schedules.exists():
            return response.Response({'message': 'Schedule overlaps with existing schedule'}, status=status.HTTP_400_BAD_REQUEST)
        
        request.data['course_plan'] = course_plan.id

        return super().create(request, *args, **kwargs)
    
    def update(self, request, *args, **kwargs):
        user = request.user
        try:
            course_plan = CoursePlan.objects.get(user=user)
        except CoursePlan.DoesNotExist:
            return response.Response({'message': 'Course plan does not exist'}, status=status.HTTP_400_BAD_REQUEST)
        
        start_time = request.data.get('start_time')
        end_time = request.data.get('end_time')
        day = request.data.get('class_day')

        if end_time <= start_time:
            return response.Response({'message': 'End time must be after start time'}, status=status.HTTP_400_BAD_REQUEST)
        
        current_schedule_id = kwargs.get('pk')

        overlapping_schedules = ClassSchedule.objects.filter(
            start_time__lt=end_time,
            end_time__gt=start_time,
            class_day=day,
            course_plan=course_plan

        ).exclude(id=current_schedule_id)

        if overlapping_schedules.exists():
            return response.Response({'message': 'Schedule overlaps with existing schedule'}, status=status.HTTP_400_BAD_REQUEST)

        request.data['course_plan'] = course_plan.id

        return super().update(request, *args, **kwargs)
    
    
class TestScheduleViewSet(viewsets.ModelViewSet):
    queryset = TestSchedule.objects.all()
    serializer_class = TestScheduleSerializer
    permission_classes = [permissions.IsAuthenticated, IsCoursePlanOwnerOrAdmin]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff or user.is_superuser:
            return TestSchedule.objects.all()
        return TestSchedule.objects.filter(course_plan__user=user)

    def create(self, request, *args, **kwargs):
        user = request.user
        try:
            course_plan = CoursePlan.objects.get(user=user)
        except CoursePlan.DoesNotExist:
            return response.Response({'message': 'Course plan does not exist'}, status=status.HTTP_400_BAD_REQUEST)
        
        test_start = request.data.get('test_start')
        test_end = request.data.get('test_end')
        date = request.data.get('test_date')

        if test_end <= test_start:
            return response.Response({'message': 'End time must be after start time'}, status=status.HTTP_400_BAD_REQUEST)
        
        overlapping_schedules = TestSchedule.objects.filter(
            test_start__lt=test_end,
            test_end__gt=test_start,
            test_date=date,
            course_plan=course_plan
        )

        if overlapping_schedules.exists():
            return response.Response({'message': 'Schedule overlaps with existing schedule'}, status=status.HTTP_400_BAD_REQUEST)
        
        request.data['course_plan'] = course_plan.id

        return super().create(request, *args, **kwargs)
    
    def update(self, request, *args, **kwargs):
        user = request.user
        try:
            course_plan = CoursePlan.objects.get(user=user)
        except CoursePlan.DoesNotExist:
            return response.Response({'message': 'Course plan does not exist'}, status=status.HTTP_400_BAD_REQUEST)

        test_start = request.data.get('test_start')
        test_end = request.data.get('test_end')
        date = request.data.get('test_date')

        if test_end <= test_start:
            return response.Response({'message': 'End time must be after start time'}, status=status.HTTP_400_BAD_REQUEST)

        current_schedule_id = kwargs.get('pk')
        
        overlapping_schedules = TestSchedule.objects.filter(
            test_start__lt=test_end,
            test_end__gt=test_start,
            test_date=date
        ).exclude(id=current_schedule_id) 

        if overlapping_schedules.exists():
            return response.Response({'message': 'Schedule overlaps with existing schedule'}, status=status.HTTP_400_BAD_REQUEST)
        
        request.data['course_plan'] = course_plan.id

        return super().update(request, *args, **kwargs)


class AssignmentDeadlineViewSet(viewsets.ModelViewSet):
    queryset = AssignmentDeadline.objects.all()
    serializer_class = AssignmentDeadlineSerializer
    permission_classes = [permissions.IsAuthenticated, IsCoursePlanOwnerOrAdmin]