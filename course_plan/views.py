from course_plan.models import AssignmentDeadline, ClassSchedule, TestSchedule, CoursePlan
from rest_framework import viewsets, response, status
from course_plan.serializers import AssignmentDeadlineSerializer, ClassScheduleSerializer, TestScheduleSerializer, CoursePlanSerializer


class CoursePlanViewSet(viewsets.ModelViewSet):
    queryset = CoursePlan.objects.all()
    serializer_class = CoursePlanSerializer
    

class ClassScheduleViewSet(viewsets.ModelViewSet):
    queryset = ClassSchedule.objects.all()
    serializer_class = ClassScheduleSerializer
    
    def create(self, request, *args, **kwargs):
        start_time = request.data.get('start_time')
        end_time = request.data.get('end_time')
        day = request.data.get('class_day')

        if end_time <= start_time:
            return response.Response({'message': 'End time must be after start time'}, status=status.HTTP_400_BAD_REQUEST)
        
        overlapping_schedules = ClassSchedule.objects.filter(
            start_time__lt=end_time,
            end_time__gt=start_time,
            class_day=day
        )

        if overlapping_schedules.exists():
            return response.Response({'message': 'Schedule overlaps with existing schedule'}, status=status.HTTP_400_BAD_REQUEST)
        
        return super().create(request, *args, **kwargs)
    
    def update(self, request, *args, **kwargs):
        start_time = request.data.get('start_time')
        end_time = request.data.get('end_time')
        day = request.data.get('class_day')

        if end_time <= start_time:
            return response.Response({'message': 'End time must be after start time'}, status=status.HTTP_400_BAD_REQUEST)
        
        overlapping_schedules = ClassSchedule.objects.filter(
            start_time__lt=end_time,
            end_time__gt=start_time,
            class_day=day
        )

        if overlapping_schedules.exists():
            return response.Response({'message': 'Schedule overlaps with existing schedule'}, status=status.HTTP_400_BAD_REQUEST)

        return super().update(request, *args, **kwargs)
    
    
class TestScheduleViewSet(viewsets.ModelViewSet):
    queryset = TestSchedule.objects.all()
    serializer_class = TestScheduleSerializer

    def create(self, request, *args, **kwargs):
        start_time = request.data.get('start_time')
        end_time = request.data.get('end_time')
        day = request.data.get('test_date')

        if end_time <= start_time:
            return response.Response({'message': 'End time must be after start time'}, status=status.HTTP_400_BAD_REQUEST)
        
        overlapping_schedules = TestSchedule.objects.filter(
            start_time__lt=end_time,
            end_time__gt=start_time,
            test_date=day
        )

        if overlapping_schedules.exists():
            return response.Response({'message': 'Schedule overlaps with existing schedule'}, status=status.HTTP_400_BAD_REQUEST)
        
        return super().create(request, *args, **kwargs)
    
    def update(self, request, *args, **kwargs):
        start_time = request.data.get('start_time')
        end_time = request.data.get('end_time')
        day = request.data.get('test_date')

        if end_time <= start_time:
            return response.Response({'message': 'End time must be after start time'}, status=status.HTTP_400_BAD_REQUEST)
        
        overlapping_schedules = TestSchedule.objects.filter(
            start_time__lt=end_time,
            end_time__gt=start_time,
            test_date=day
        )

        if overlapping_schedules.exists():
            return response.Response({'message': 'Schedule overlaps with existing schedule'}, status=status.HTTP_400_BAD_REQUEST)
        

        return super().update(request, *args, **kwargs)


class AssignmentDeadlineViewSet(viewsets.ModelViewSet):
    queryset = AssignmentDeadline.objects.all()
    serializer_class = AssignmentDeadlineSerializer