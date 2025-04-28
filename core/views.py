from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.template.loader import render_to_string
from weasyprint import HTML
from django.http import FileResponse
from django.db.models import Avg, Count
from django.db.models.functions import TruncDate
from django.conf import settings
from .models import FrequentQuestions, UserReport, UserProfile, FrequentQuestions
from django.http import Http404
import plotly.graph_objs as go
import plotly.offline as opy
import io
from .models import HelpRequest, UserProfile
import re
import os
import json

# List of common passwords to block (you can expand this list)
COMMON_PASSWORDS = [
    'welcome123', 'monkey123', 'football123', 'abc123456', 'password1',
    '123456789', '1234567', '#Password1', '123456', '1234567890',   'password123', 'admin123', '12345678', 'qwerty123', 'letmein123',
  '12345',
    'qwertyuiop', 'qwerty', '123321',
]

PHISHING_SIM_PATH = 'dashboard/phishing_sims/'
PHISHING_SIM_ANSWERS_PATH = 'phishing_training/quiz_answer_maps/'

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
    user = request.user
    top_questions = (
        FrequentQuestions.objects
        .values('question')
        .annotate(count=Count('question'))
        .order_by('-count')[:5]
    )

    context = {
        'daily_averages': dashboard_daily_scores(),
        'total_reports': dashboard_total_reports(),
        'user_rating': dashboard_user_rating(user),
        'user_reports': dashboard_user_reports(user),
        'questions': top_questions,
    }

    return render(request, 'dashboard/dashboard.html', context)

def dashboard_daily_scores():
    daily_averages = (
        UserReport.objects
        .annotate(date=TruncDate('time_stamp'))
        .values('date')
        .annotate(avg_score=Avg('score'))
        .order_by('date')
    )

    if not daily_averages:
        return None

    # Separate into x and y data
    x = [entry['date'].strftime('%Y-%m-%d') for entry in daily_averages]
    y = [round(entry['avg_score'] * 100, 2) if entry['avg_score'] is not None else 0 for entry in daily_averages]

    # Plotly Bar Chart
    trace = go.Bar(x=x, y=y, marker_color='#3498db')
    layout = go.Layout(
        xaxis=dict(title='Date'),
        yaxis=dict(title='Average Score', range=[0, 100], tick0=0, dtick=10),
        height=300,
    )
    fig = go.Figure(data=[trace], layout=layout)
    chart_div = opy.plot(fig, auto_open=False, output_type='div')
    return chart_div

def dashboard_total_reports():
    report_counts = (
        UserReport.objects
        .values('user__role')
        .annotate(total=Count('id'))
    )

    if not report_counts:
        return None

    total_reports = UserReport.objects.count()
    

    labels = [entry['user__role'].capitalize() for entry in report_counts]
    values = [entry['total'] for entry in report_counts]

    layout = go.Layout(
        height=200,
        margin=dict(t=50, b=50, l=50, r=50),
        autosize=True,
        legend=dict(
            orientation="v",    # vertical list
            x=0,                # far left
            y=0,                # bottom
            xanchor='left',
            yanchor='bottom'
        ),
    )
    fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=0.5)], layout=layout)

    fig.update_layout(
    showlegend=True,

    annotations=[dict(
        text=f'{total_reports}',
        x=0.5,
        y=0.5,
        font_size=20,
        showarrow=False,
        align='center'
    )],
    )

    pie_chart = opy.plot(fig, output_type='div')
    return pie_chart

def dashboard_user_rating(user):
    user_profile = get_object_or_404(UserProfile, user=user)
    user_reports = UserReport.objects.filter(user=user_profile)

    if not user_reports:
        return None

    x = [report.difficulty.capitalize() for report in user_reports]
    
    # Ensure 'y' values (score) are valid numbers, replacing None with 0 or a default value
    y = [float(report.score) if report.score is not None else 0 for report in user_reports]

    size = []
    for report in user_reports:
        # Ensure that 'responses' is not None and has the 'clicked_links' key
        if report.responses and isinstance(report.responses, dict):
            size.append(report.responses.get('clicked_links', 5))  # Default to 5 if 'clicked_links' is missing
        else:
            size.append(5)  # Default to 5 if 'responses' is None or not a dict

    text = [report.difficulty.capitalize() for report in user_reports]

    trace = go.Scatter(
        x=x,
        y=y,
        text=text,
        mode='markers',
        marker=dict(
            size=size,
            color=y,  # Use 'y' values for color
            colorscale='Viridis',
            showscale=True,
            opacity=0.7,
            sizemode='area',
            sizeref=2.*max(size)/(40.**2),  # controls scale of bubbles
            sizemin=4,
        )
    )

    layout = go.Layout(
        xaxis=dict(title='Number of Questions'),
        yaxis=dict(title='Score'),
        height=400,
    )

    fig = go.Figure(data=[trace], layout=layout)
    bubble_plot = opy.plot(fig, auto_open=False, output_type='div')
    return bubble_plot

def dashboard_user_reports(user):
    user_profile = get_object_or_404(UserProfile, user=user)
    
    # Now use the UserProfile for querying UserReport
    reports = UserReport.objects.filter(user=user_profile).order_by('time_stamp')

    if not reports:
        return None

    # Extract data
    dates = [report.time_stamp.strftime('%Y-%m-%d') for report in reports]
    scores = [report.score for report in reports]

    # Create Plotly Line Chart
    trace = go.Scatter(x=dates, y=scores, mode='lines+markers', name='Score', line=dict(color='green'))
    layout = go.Layout(
        title='Your Report Scores Over Time',
        xaxis=dict(title='Date'),
        yaxis=dict(title='Score', range=[0, 100]),
        height=200,
        margin=dict(t=30, b=40, l=40, r=30),
    )

    fig = go.Figure(data=[trace], layout=layout)
    line_chart = opy.plot(fig, output_type='div', auto_open=False)
    return line_chart

@login_required
def training(request):
    return render(request, 'dashboard/training.html')

@login_required
def quiz_selection(request):
    if request.method == 'POST':
        difficulty = request.POST.get('action')
        request.session['selected_difficulty'] = difficulty
        return redirect('quiz')  # Assuming 'quiz' is your existing view name

    return render(request, 'dashboard/quiz_selection.html')

@login_required
def quiz(request):
    user = request.user
    user_profile = get_object_or_404(UserProfile, user=user)
    difficulty = request.session.get('selected_difficulty', 'easy')
    sim_dir = os.path.join(settings.TEMPLATES[0]['DIRS'][0], PHISHING_SIM_PATH, difficulty)
    sim_files = sorted([f for f in os.listdir(sim_dir) if f.endswith('.html')])
    total_questions = len(sim_files)/2
    next_button = 'Next'
    print(difficulty)

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
        score = grade_quiz(responses, difficulty)
        clicks = request.session.get('clicked_phish_link', [])
        report = UserReport.objects.create(
            user=user_profile,
            difficulty=difficulty,
            responses={
                'responses': responses,
                'links_clicked': clicks,
            },
            num_questions=total_questions,
            score=score,
        )
        # Flush quiz session variables
        for key in ['quiz_index', 'quiz_responses', 'clicked_phish_link', 'show_fake_site']:
            request.session.pop(key, None)
        return render(request, 'dashboard/quiz_result.html', {
            'report': report,
            'score': score*100,
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
        elif action == 'back':
            for key in ['quiz_index', 'quiz_responses', 'clicked_phish_link', 'show_fake_site', 'selected_difficulty']:
                request.session.pop(key, None)
            return redirect('quiz-selection')
        print(index) 
        return redirect('quiz')

    return render(request, 'dashboard/quiz.html', {
        'sim_template': sim_template,
        'question_number': index + 1,
        'total': total_questions,
        'next_button': next_button,
        'difficulty': difficulty.capitalize(),
    })

def grade_quiz(responses, difficulty):
    # Load the correct answers
    answer_file = os.path.join(settings.BASE_DIR, PHISHING_SIM_ANSWERS_PATH, f'{difficulty}.json')
    with open(answer_file) as f:
        correct_answers = json.load(f)

    total = len(correct_answers)
    correct = 0

    for i, user_answer in enumerate(responses, start=1):
        if str(i) in correct_answers and user_answer == correct_answers[str(i)]:
            correct += 1

    score = correct / total if total > 0 else 0
    return score

@login_required
def phishing_clicked(request, question_number):
    # Track the click
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

    if request.method == "POST":
        difficulty = request.POST.get('action')
        print(difficulty)
        report = generate_report(request, user_profile, difficulty)
        return report

    return render(request, 'dashboard/report.html' )

@login_required
def generate_report(request, user_profile, difficulty):
    # Query the UserReport
    print(user_profile, difficulty)
    report = UserReport.objects.filter(user=user_profile, difficulty=difficulty).order_by('-time_stamp').first()
    # Render HTML
    if not report:
        messages.error(request, f"No reports for this difficulty. Take a {difficulty} quiz.")
        return render(request, 'dashboard/report.html')
    
    html_string = render_to_string('dashboard/quiz_report.html', {'report': report,
                                                                    'score': report.score *100})
    html = HTML(string=html_string)

    # Generate PDF
    pdf_file = html.write_pdf()
    file_name = f'quiz_report_{difficulty}.pdf'
    pdf_buffer = io.BytesIO(pdf_file)
    # Return PDF as response
    return FileResponse(pdf_buffer, as_attachment=True, filename=file_name)    

@login_required
def user_settings(request):
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
    user = request.user
    context = {
        'user_rating': dashboard_user_rating(user),
        'user_reports': dashboard_user_reports(user),
        'user': user,
    }
    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'change_profile':
            return change_profile(request, user)
        elif action == 'change_pass':
            return change_pass(request, user)

    return render(request, 'dashboard/profile.html', context)

@login_required
def change_profile(request, user):
    full_name = request.POST.get('name', '')
    username = request.POST.get('username', '')
    email = request.POST.get('email', '')

    if full_name:
        names = full_name.strip().split(' ', 1)
        user.first_name = names[0]
        user.last_name = names[1] if len(names) > 1 else ''

    if username:
        user.username = username

    if email:
        user.email = email

    user.save()
    messages.success(request, 'Profile updated successfully.')
    return redirect('profile')    

@login_required
def change_pass(request, user):
    old_pass = request.POST.get('old-pass')
    new_pass = request.POST.get('new-pass')
    confirm_pass = request.POST.get('confirm-pass')
    print(new_pass)
    print(confirm_pass)

    if not user.check_password(old_pass):
        messages.error(request, 'Old password is incorrect.')
        return redirect('profile')

    if new_pass != confirm_pass:
        messages.error(request, 'New passwords do not match.')
        return redirect('profile')

    pass_valid = validate_password_strength(new_pass, user.username, user.email)

    if not pass_valid:
        messages.error(request, pass_valid)
        return redirect('profile')
        
    user.set_password(new_pass)
    user.save()
    update_session_auth_hash(request, user)  # Keep user logged in

    messages.success(request, 'Password updated successfully.')
    return redirect('profile')

@login_required
def dashboard_help(request):
    if request.method == 'POST':
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        if not subject or not message:
            messages.error(request, "Please fill in both subject and message.")
        else:
            HelpRequest.objects.create(
                user=request.user,
                subject=subject,
                message=message
            )
            messages.success(request, "Your help request has been submitted successfully.")

    return render(request, 'dashboard/help.html')

@login_required
def template(request): #don't update this view
    return render(request, 'dashboard/template.html')