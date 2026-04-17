from django.contrib import admin
from django.urls import path, include  # <-- Notice we added 'include' here

urlpatterns = [
    path('admin/', admin.site.urls),
    # This connects the main highway to your app's local roads:
    path('', include('predictor.urls')), 
]