"""
URL configuration for core app.
"""
from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('health/', views.health_check, name='health_check'),
    path('ping/', views.ping, name='ping'),
    path('readiness/', views.readiness, name='readiness'),
]