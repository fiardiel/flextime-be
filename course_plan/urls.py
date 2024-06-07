from django.urls import path, include
from rest_framework import routers
from course_plan import views

router = routers.DefaultRouter()
router.register(r'class-schedule', views.ClassScheduleViewSet)
router.register(r'test-schedule', views.TestScheduleViewSet)
router.register(r'assignment-deadline', views.AssignmentDeadlineViewSet)
router.register(r'course-plan', views.CoursePlanViewSet)

urlpatterns = [
    path('', include(router.urls)),
]