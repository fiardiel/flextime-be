# Generated by Django 5.0.6 on 2024-06-02 07:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("fitness_plan", "0002_remove_sessionplan_trainings"),
    ]

    operations = [
        migrations.RenameModel(
            old_name="SessionPlanTraining",
            new_name="SessionTraining",
        ),
    ]
