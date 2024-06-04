from django.db import models
from datetime import time

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
    start_time = models.TimeField(default=time(0,0))
    end_time = models.TimeField(default=time(0,0))
    class_day = models.CharField(max_length=3, choices=DAYS_OF_WEEK)


class TestSchedule(models.Model):
    test_name = models.CharField(max_length=255)
    test_date = models.DateField()
    test_start = models.TimeField(default=time(0,0))
    test_end = models.TimeField(default=time(0,0))

class AssignmentDeadline(models.Model):
    assignment_name = models.CharField(max_length=255)
    assignment_due_date = models.DateTimeField()
