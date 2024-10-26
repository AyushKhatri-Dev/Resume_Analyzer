from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.upload_resume, name='upload_resume'),
    path('analysis/<int:pk>/', views.view_analysis, name='view_analysis'),
    
    # Authentication URLs
    path('signup/', views.sign_up, name='signup'),
    path('signin/', views.sign_in, name='signin'),
    path('logout/', views.log_out, name='logout'),
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='resume_analyzer/password_reset.html'), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='resume_analyzer/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='resume_analyzer/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='resume_analyzer/password_reset_complete.html'), name='password_reset_complete'),
]
