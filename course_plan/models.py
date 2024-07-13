from django.db import models
from django.contrib.auth.models import User

class CoursePlan(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
class ClassSchedule(models.Model):
    DAYS_OF_WEEK = [
        ('MON', 'Monday'),
        ('TUE', 'Tuesday'),
        ('WED', 'Wednesday'),
        ('THU', 'Thursday'),
        ('FRI', 'Friday'),
        ('SAT', 'Saturday'),
        ('SUN', 'Sunday'),
    ]

    class_name = models.CharField(max_length=255)
    start_time = models.TimeField()
    end_time = models.TimeField()
    class_day = models.CharField(max_length=3, choices=DAYS_OF_WEEK)
    course_plan = models.ForeignKey(CoursePlan, on_delete=models.CASCADE)

    class Meta:
        ordering = ['start_time']


class TestSchedule(models.Model):
    test_name = models.CharField(max_length=255)
    test_date = models.DateField()
    test_start = models.TimeField()
    test_end = models.TimeField()
    course_plan = models.ForeignKey(CoursePlan, on_delete=models.CASCADE)

class AssignmentDeadline(models.Model):
    assignment_name = models.CharField(max_length=255)
    assignment_due_date = models.DateField()
    assignment_due_time = models.TimeField()
    course_plan = models.ForeignKey(CoursePlan, on_delete=models.CASCADE)
