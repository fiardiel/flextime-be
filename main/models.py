from django.db import models
from users.models import User
from fitness_plan.models import SessionPlan, FitnessPlan
from course_plan.models import CoursePlan

class ActivityPlan(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    course_plan = models.OneToOneField(CoursePlan, on_delete=models.CASCADE)
    fitness_plan = models.OneToOneField(FitnessPlan, on_delete=models.CASCADE)

class SessionSchedule(models.Model):
    DAYS_OF_WEEK = [
        ('MON', 'Monday'),
        ('TUE', 'Tuesday'),
        ('WED', 'Wednesday'),
        ('THU', 'Thursday'),
        ('FRI', 'Friday'),
        ('SAT', 'Saturday'),
        ('SUN', 'Sunday'),
    ]

    session_plan = models.OneToOneField(SessionPlan, on_delete=models.CASCADE)
    activity_plan = models.ForeignKey(ActivityPlan, on_delete=models.CASCADE)
    start_time = models.TimeField()
    end_time = models.TimeField()
    day = models.CharField(max_length=3, choices=DAYS_OF_WEEK)