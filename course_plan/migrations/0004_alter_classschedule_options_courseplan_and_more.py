# Generated by Django 5.0.6 on 2024-06-07 12:12

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("course_plan", "0003_classschedule_class_day"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="classschedule",
            options={"ordering": ["start_time"]},
        ),
        migrations.CreateModel(
            name="CoursePlan",
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
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="assignmentdeadline",
            name="course_plan",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                to="course_plan.courseplan",
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="classschedule",
            name="course_plan",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                to="course_plan.courseplan",
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="testschedule",
            name="course_plan",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                to="course_plan.courseplan",
            ),
            preserve_default=False,
        ),
    ]
