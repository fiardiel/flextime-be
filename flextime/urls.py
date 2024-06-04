from django.urls import path, include
from main import views as main_views
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'users', main_views.UserViewSet)
router.register(r'groups', main_views.GroupViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('', include('fitness_plan.urls')),
    path('', include('course_plan.urls')),
    path('api-auth/', include('rest_framework.urls', 'rest_framework')),
]
