from django.urls import path, include

urlpatterns = [
    path('', include('main.urls')),
    path('', include('fitness_plan.urls')),
    path('', include('course_plan.urls')),
    path('', include('users.urls')),
    path('api-auth/', include('rest_framework.urls', 'rest_framework')),
]
