from django.urls import path, include
from rest_framework import routers
from main import views

router = routers.DefaultRouter()
router.register(r'group', views.GroupViewSet)
router.register(r'activity-plan', views.ActivityPlanViewSet)
router.register(r'session-schedule', views.SessionScheduleViewSet)

urlpatterns = [
    path('', include(router.urls)),
]