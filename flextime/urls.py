from django.urls import path, include
from rest_framework import routers
from fitness_plan import views as fitness_plan_views
from main import views as main_views

router = routers.DefaultRouter()
router.register(r'users', main_views.UserViewSet)
router.register(r'groups', main_views.GroupViewSet)
router.register(r'fitnessplans', fitness_plan_views.FitnessPlanViewSet)
router.register(r'sessionplans', fitness_plan_views.SessionPlanViewSet)
router.register(r'trainings', fitness_plan_views.TrainingViewSet)
router.register(r'customizations', fitness_plan_views.CustomizationViewSet)
router.register(r'sessiontrainings', fitness_plan_views.SessionTrainingViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', 'rest_framework')),
]
