from django.contrib import admin
from django.urls import path
from .views import QuizView, SettingsView

urlpatterns = [
    path('quiz/', QuizView.as_view(), name='quiz'),
    path('settings/', SettingsView.as_view(), name='settings'),
]
