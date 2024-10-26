from django.urls import path
from . import views

urlpatterns = [
    path('', views.upload_resume, name='upload_resume'),
    path('analysis/<int:pk>/', views.view_analysis, name='view_analysis'),
    
    # Authentication URLs
    path('signup/', views.sign_up, name='signup'),
    path('signin/', views.sign_in, name='signin'),
    path('logout/', views.log_out, name='logout'),
]
