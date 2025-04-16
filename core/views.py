from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.template.loader import render_to_string
from weasyprint import HTML
from django.http import FileResponse
import re
import os
from django.conf import settings
from .models import UserReport, UserProfile

# List of common passwords to block (you can expand this list)
COMMON_PASSWORDS = [
    'welcome123', 'monkey123', 'football123', 'abc123456', 'password1', 
    '123456789', '1234567', '#Password1', '123456', '1234567890',   'password123', 'admin123', '12345678', 'qwerty123', 'letmein123',
  '12345', 
    'qwertyuiop', 'qwerty', '123321',
]

PHISHING_SIM_PATH = 'dashboard/phishing_sims/'

def validate_password_strength(password, username, email):
    """
    Validate password strength with custom rules.
    Returns None if valid, or an error message if invalid.
    """
    # Minimum length (already enforced in settings.py, but we'll check here too)
    if len(password) < 8:
        return "Password must be at least 8 characters long."

    # Check for at least one uppercase letter, one lowercase letter, one digit, and one special character
    if not re.search(r'[A-Z]', password):
        return "Password must contain at least one uppercase letter."
    if not re.search(r'[a-z]', password):
        return "Password must contain at least one lowercase letter."
    if not re.search(r'[0-9]', password):
        return "Password must contain at least one digit."
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        return "Password must contain at least one special character (e.g., !@#$%^&*)."

    # Check if password is too similar to username or email
    username_lower = username.lower()
    email_lower = email.lower().split('@')[0]  # Get the part before the @ in the email
    password_lower = password.lower()
    if username_lower in password_lower or email_lower in password_lower:
        return "Password cannot contain your username or email."

    # Check for common passwords
    if password_lower in [cp.lower() for cp in COMMON_PASSWORDS]:
        return "This password is too common. Please choose a more unique password."

    return None  # Password is valid


# front-end views
def index(request):
    return render(request, 'index.html')

# Sign-in views
def signin(request):
    if request.user.is_authenticated:
        return redirect('dashboard')  # Redirect if already logged in

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Basic input validation
        if not username or not password:
            messages.error(request, "Please provide both username and password.")
            return render(request, 'signin.html')

        # Check if the username exists
        try:
            user = User.objects.get(username=username)
            # Username exists, try to authenticate
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Welcome back, {username}!")
                return redirect('dashboard')
            else:
                messages.error(request, "The password you entered is incorrect.")
                return render(request, 'signin.html')
        except User.DoesNotExist:
            messages.error(request, "The username does not exist.")
            return render(request, 'signin.html')

    return render(request, 'signin.html')

# Signup Views
def signup(request):
    if request.user.is_authenticated:
        return redirect('dashboard')  # Redirect if already logged in

    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        # Input validation
        if not all([username, email, password, confirm_password]):
            messages.error(request, "All fields are required.")
            return render(request, 'signup.html')

        # Username validation (alphanumeric and underscores, 3-30 characters)
        if not re.match(r'^[a-zA-Z0-9_]{3,30}$', username):
            messages.error(request, "Username must be 3-30 characters long and contain only letters, numbers, or underscores.")
            return render(request, 'signup.html')

        # Email validation
        if not re.match(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', email):
            messages.error(request, "Please enter a valid email address.")
            return render(request, 'signup.html')

        # Password validation: Check if passwords match
        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return render(request, 'signup.html')

        # Password strength validation
        password_error = validate_password_strength(password, username, email)
        if password_error:
            messages.error(request, password_error)
            return render(request, 'signup.html')

        # Check if username or email already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return render(request, 'signup.html')
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists.")
            return render(request, 'signup.html')

        try:
            # Create user
            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()
            messages.success(request, "Sign-up successfully! Please log in.")
            return redirect('signin')
        except ValidationError as e:
            messages.error(request, f"Error creating account: {str(e)}")
            return render(request, 'signup.html')

    return render(request, 'signup.html')

#Logout views
def logout_view(request):
    # print(f"Logout request method: {request.method}")  # Debug
    if request.method == 'POST':
        logout(request)
        messages.success(request, "You have been logged out successfully.")
        return redirect('index')
    else:
        return redirect('dashboard')


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

def user_settings(request):
    return render(request, 'dashboard/settings.html')

def template(request):
    return render(request, 'dashboard/template.html')

def training(request):
    return render(request, 'dashboard/training.html')


# Dashboard views (all protected with @login_required)
# For security and privacy purposes, all user must be logged in to view the dashboard pages
@login_required
def dashboard(request):
    return render(request, 'dashboard/dashboard.html')

@login_required
def training(request):
    return render(request, 'dashboard/training.html')

@login_required
def quiz(request):
    user = request.user
    user_profile = get_object_or_404(UserProfile, user=user)
    difficulty = 'easy'
    sim_dir = os.path.join(settings.TEMPLATES[0]['DIRS'][0], PHISHING_SIM_PATH, difficulty)
    sim_files = sorted([f for f in os.listdir(sim_dir) if f.endswith('.html')])
    total_questions = len(sim_files)/2
    next_button = 'Next'

    # First question
    if 'quiz_index' not in request.session:
        request.session['quiz_index'] = 0
        request.session['quiz_responses'] = []
        request.session['clicked_phish_link'] = []

    index = request.session['quiz_index']

    # Last question
    if index >= total_questions-1:
        next_button = 'Submit'
    else:
        next_button = 'Next'

    # Quiz finished
    if index >= total_questions:
        responses = request.session.get('quiz_responses', [])
        clicks = request.session.get('clicked_phish_link', [])
        report = UserReport.objects.create(
            user=user_profile,
            difficulty=difficulty,
            report_type='quiz',
            responses={
                'responses': responses,
                'links_clicked': clicks,
            },
            num_questions=total_questions,
            score=0.5,
        )
        # Flush quiz session variables
        for key in ['quiz_index', 'quiz_responses', 'clicked_phish_link', 'show_fake_site']:
            request.session.pop(key, None)
        return render(request, 'dashboard/quiz_result.html', {
            'report': report,
        })

    # Determine what to include: email or fake site
    if request.session.get('show_fake_site', False):
        sim_template = f"{sim_dir}/{index + 1}-site.html"
    else:
        sim_template = f"{sim_dir}/{index + 1}.html"

    # Handle form submission
    if request.method == 'POST':
        action = request.POST.get('action')
    
        # If user clicked 'Next', save answer and move forward
        if action == 'next':
            answer = request.POST.get('answer')
            responses = request.session.get('quiz_responses', [])
            if len(responses) > index:
                responses[index] = answer  # update existing
            else:
                responses.append(answer)
            request.session['quiz_responses'] = responses
            request.session['quiz_index'] += 1
            request.session['show_fake_site'] = False

        # If user clicked 'Previous', just go back (don't change answers here)
        elif action == 'previous':
            request.session['quiz_index'] = max(0, index - 1)
            request.session['show_fake_site'] = False
        print(index) 
        return redirect('quiz')

    return render(request, 'dashboard/quiz.html', {
        'sim_template': sim_template,
        'question_number': index + 1,
        'total': total_questions,
        'next_button': next_button,
    })

def grade_quiz(responses):
    ...

@login_required
def phishing_clicked(request, question_number):
    # Track it
    clicked = request.session.get('clicked_phish_link', [])
    if int(question_number) not in clicked:
        clicked.append(int(question_number))
        request.session['clicked_phish_link'] = clicked

    # Show fake site
    request.session['show_fake_site'] = True
    return redirect('quiz')

@login_required
def report(request):
    user = request.user
    user_profile = get_object_or_404(UserProfile, user=user)
    user_report = get_object_or_404(UserReport, user=user_profile, difficulty='easy', report_type='quiz')

    return render(request, 'dashboard/report.html', {'report': user_report})

@login_required
def generate_report(request, report_type, difficulty):
        # Get the UserProfile instance
    user = request.user
    user_profile = get_object_or_404(UserProfile, user=user)

    # Query the UserReport
    report = get_object_or_404(
        UserReport,
        user=user_profile,
        difficulty=difficulty,
        report_type=report_type  # or 'training' if you need that instead
    )
    # Render HTML
    html_string = render_to_string('dashboard/quiz_result.html', {'report': report})
    html = HTML(string=html_string)

    # Generate PDF
    pdf_file = html.write_pdf()
    file_name = f'quiz_report_{report_type}_{difficulty}.pdf'
    # Return PDF as response
    return FileResponse(pdf_file, as_attachment=True, filename=file_name)    

@login_required
def user_settings(request):
    return render(request, 'dashboard/settings.html')

@login_required
def profile(request):
    return render(request, 'dashboard/profile.html')

@login_required
def dashboard_help(request):
    return render(request, 'dashboard/help.html')

@login_required
def template(request): #don't update this view
    return render(request, 'dashboard/template.html')