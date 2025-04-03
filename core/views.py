from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# front-end views
def index(request):
    return render(request, 'index.html')

def signin(request):
    return render(request, 'signin.html')

def signup(request):
    return render(request, 'signup.html')

def privacy(request):
    return render(request, 'privacy.html')

def terms(request):
    return render(request, 'terms.html')

def help(request):
    return render(request, 'help.html')

def documentation(request):
    return render(request, 'documentation.html')

def dashboard(request):
    return render(request, 'dashboard/dashboard.html')

def dashboard_help(request):
    return render(request, 'dashboard/help.html')

def profile(request):
    return render(request, 'dashboard/profile.html')

def quiz(request):
    return render(request, 'dashboard/quiz.html')

def report(request):
    return render(request, 'dashboard/report.html')

def settings(request):
    return render(request, 'dashboard/settings.html')

def template(request):
    return render(request, 'dashboard/template.html')

def training(request):
    return render(request, 'dashboard/training.html')


# dashboard views

# @login_required
def dashboard(request):
    return render(request, 'dashboard/dashboard.html')

def training(request):
    return render(request, 'dashboard/training.html')

def quiz(request):
    return render(request, 'dashboard/quiz.html')

def report(request):
    return render(request, 'dashboard/report.html')

def settings(request):
    return render(request, 'dashboard/settings.html')

def profile(request):
    return render(request, 'dashboard/profile.html')

def help(request):
    return render(request, 'dashboard/help.html')

def template(request): #don't update this view
    return render(request, 'dashboard/template.html')