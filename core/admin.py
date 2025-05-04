from django.contrib import admin
from .models import UserReport, FrequentQuestions, InitalQuizQuestions

# Register your models here.
admin.site.register(UserReport)
admin.site.register(FrequentQuestions)
admin.site.register(InitalQuizQuestions)