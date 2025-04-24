from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from .models import HelpRequest, UserProfile
import re

# List of common passwords to block (you can expand this list)
COMMON_PASSWORDS = [
    'welcome123', 'monkey123', 'football123', 'abc123456', 'password1',
    '123456789', '1234567', '#Password1', '123456', '1234567890',   'password123', 'admin123', '12345678', 'qwerty123', 'letmein123',
  '12345',
    'qwertyuiop', 'qwerty', '123321',
]

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

def settings(request):
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
    return render(request, 'dashboard/quiz.html')

@login_required
def report(request):
    return render(request, 'dashboard/report.html')

@login_required
def settings(request):
    if request.method == 'POST':
        # Extract form data
        theme = request.POST.get('theme')
        difficulty = request.POST.get('difficulty')
        share_score = request.POST.get('share-score') == 'on'  # Convert checkbox to boolean
        share_progress = request.POST.get('share-progress') == 'on'
        feedback = request.POST.get('feedback')

        # Save the user settings in the database
        user_profile = request.user.profile  # Get the related UserProfile

        # Update profile fields
        user_profile.theme = theme
        user_profile.difficulty = difficulty
        user_profile.share_score = share_score
        user_profile.share_progress = share_progress
        user_profile.feedback = feedback

        user_profile.save()

        messages.success(request, "Your settings have been updated successfully.")

        # Redirect back to the settings page (to show a success message)
        return redirect('settings')

    return render(request, 'dashboard/settings.html', {'profile': profile})

@login_required
def profile(request):
    return render(request, 'dashboard/profile.html')

@login_required
def help(request):
    if request.method == 'POST':
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        user_email = request.user.email if request.user.is_authenticated else 'support@phishingtool.com'

        # Basic validation
        if not subject or not message:
            messages.error(request, "Please fill in both subject and message.")
        else:
            try:
                # Define standard email components
                send_mail(
                    subject=f"[Help Request] {subject}",
                    message=f"From: {user_email}\n\nMessage:\n{message}",
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[settings.SUPPORT_EMAIL],
                    fail_silently=False,
                )
                messages.success(request,
                                 "Your message has been sent successfully. Our team will get back to you shortly.")
            except Exception as e:
                messages.error(request, f"An error occurred while sending your message: {e}")

    return render(request, 'help.html')

@login_required
def template(request): #don't update this view
    return render(request, 'dashboard/template.html')

