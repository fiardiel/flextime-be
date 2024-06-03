from django.db import models
from django.contrib.auth.models import User

class FitnessPlan(models.Model):
    title = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class Customization(models.Model):
    reps = models.IntegerField()
    sets = models.IntegerField()
    duration = models.IntegerField()

class Training(models.Model):
    title = models.CharField(max_length=255)
    training_type = models.CharField(max_length=255)
    description = models.TextField() 

class SessionPlan(models.Model):
    training_type = models.CharField(max_length=255)
    fitness_plan = models.ForeignKey(FitnessPlan, on_delete=models.CASCADE)

class SessionTraining(models.Model):
    session_plan = models.ForeignKey(SessionPlan, on_delete=models.CASCADE)
    training = models.ForeignKey(Training, on_delete=models.CASCADE)
    customization = models.OneToOneField(Customization, on_delete=models.CASCADE, null=True, blank=True)
