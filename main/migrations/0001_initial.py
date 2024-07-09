# Generated by Django 5.0.6 on 2024-06-08 02:32

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("course_plan", "0001_initial"),
        ("fitness_plan", "0004_alter_sessiontraining_unique_together"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="ActivityPlan",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "course_plan",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="course_plan.courseplan",
                    ),
                ),
                (
                    "fitness_plan",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="fitness_plan.fitnessplan",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="SessionSchedule",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("start_time", models.TimeField()),
                ("end_time", models.TimeField()),
                (
                    "day",
                    models.CharField(
                        choices=[
                            ("MON", "Monday"),
                            ("TUE", "Tuesday"),
                            ("WED", "Wednesday"),
                            ("THU", "Thursday"),
                            ("FRI", "Friday"),
                            ("SAT", "Saturday"),
                            ("SUN", "Sunday"),
                        ],
                        max_length=3,
                    ),
                ),
                (
                    "activity_plan",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="main.activityplan",
                    ),
                ),
                (
                    "session_plan",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="fitness_plan.sessionplan",
                    ),
                ),
            ],
        ),
    ]