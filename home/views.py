from django import template
from django.shortcuts import render
from django.views.generic import TemplateView


# Create your views here.

class QuizView(TemplateView):
    template_name = 'quiz.html'

class SettingsView(TemplateView):
    template_name = 'settings.html'