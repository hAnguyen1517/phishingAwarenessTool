from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('signin/', views.signin, name='signin'),
    path('signup/', views.signup, name='signup'),
    path('logout/', views.logout_view, name='logout'),
    path('privacy/', views.privacy, name='privacy'),
    path('terms/', views.terms, name='terms'),
    path('help/', views.help, name='help'),
    path('documentation/', views.documentation, name='documentation'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard/help/', views.dashboard_help, name='dashboard_help'),
    path('dashboard/profile/', views.profile, name='profile'),
    path('dashboard/quiz/', views.quiz, name='quiz'),
    path('dashboard/quiz-selection/', views.quiz_selection, name='quiz-selection'),
    path('quiz/phish-clicked/<int:question_number>/', views.phishing_clicked, name='phishing_clicked'),
    path('dashboard/report/', views.report, name='report'),
    path('dashboard/report/<str:report_type>/<str:difficulty>/', views.generate_report, name='generate_report'),
    path('dashboard/settings/', views.user_settings, name='settings'),
    path('dashboard/template/', views.template, name='template'),
    path('dashboard/training/', views.training, name='training'),
]