from rest_framework import serializers
from course_plan.models import AssignmentDeadline, ClassSchedule, TestSchedule


class AssignmentDeadlineSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssignmentDeadline
        fields = '__all__'

class ClassScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClassSchedule
        fields = '__all__'

class TestScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestSchedule
        fields = '__all__'
