from django.urls import path, include
from main import views as main_views
from rest_framework import routers

urlpatterns = [
    path('', include('main.urls')),
    path('', include('fitness_plan.urls')),
    path('', include('course_plan.urls')),
    path('api-auth/', include('rest_framework.urls', 'rest_framework')),
]
