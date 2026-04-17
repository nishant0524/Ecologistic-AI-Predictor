from django.urls import path
from . import views

urlpatterns = [
    # This means: "When someone goes to the homepage, run the predict_emissions view"
    path('', views.predict_emissions, name='predict'),
]