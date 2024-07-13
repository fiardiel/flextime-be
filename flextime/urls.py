from django.urls import path, include
from django.contrib import admin

urlpatterns = [
    path('', include('main.urls')),
    path('', include('fitness_plan.urls')),
    path('', include('course_plan.urls')),
    path('', include('authentication.urls')),
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls', 'rest_framework')),
]
