from django.urls import path, include
from rest_framework import routers
from fitness_plan import views as fitness_plan_views

router = routers.DefaultRouter()
router.register(r'fitness-plan', fitness_plan_views.FitnessPlanViewSet)
router.register(r'session-plan', fitness_plan_views.SessionPlanViewSet)
router.register(r'training', fitness_plan_views.TrainingViewSet)
router.register(r'customization', fitness_plan_views.CustomizationViewSet)
router.register(r'session-training', fitness_plan_views.SessionTrainingViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
