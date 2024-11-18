from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # Admin page
    path('admin/', admin.site.urls),

    # API endpoint for accessing all the views and routes for the API
    path('api/', include('api.urls')),  # Include API routes from the api app

    # Health app endpoint for general health-related routes
    path('healthapp/', include('healthapp.urls')),  # Include routes for healthapp
]
