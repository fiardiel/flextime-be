from course_plan.models import AssignmentDeadline, ClassSchedule, TestSchedule
from rest_framework import viewsets, response, status
from course_plan.serializers import AssignmentDeadlineSerializer, ClassScheduleSerializer, TestScheduleSerializer
from rest_framework.decorators import action


class ClassScheduleViewSet(viewsets.ModelViewSet):
    queryset = ClassSchedule.objects.all()
    serializer_class = ClassScheduleSerializer

class TestScheduleViewSet(viewsets.ModelViewSet):
    queryset = TestSchedule.objects.all()
    serializer_class = TestScheduleSerializer

class AssignmentDeadlineViewSet(viewsets.ModelViewSet):
    queryset = AssignmentDeadline.objects.all()
    serializer_class = AssignmentDeadlineSerializer