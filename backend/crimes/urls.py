from django.urls import path
from . import views

urlpatterns = [
    path('data/', views.crimes, name='crime_data'),
]