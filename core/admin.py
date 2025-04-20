from django.contrib import admin
from .models import UserReport, FrequentQuestions

# Register your models here.
admin.site.register(UserReport)
admin.site.register(FrequentQuestions)
