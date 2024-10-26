from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from .models import Resume
from .forms import SignUpForm, SignInForm
from django.contrib import messages
from .utils import analyze_resume  # Import the analyze_resume function


def upload_resume(request):
    if request.method == 'POST':
        resume_file = request.FILES.get('resume')
        job_role = request.POST.get('job_role')
        
        if resume_file and job_role:
            resume = Resume.objects.create(
                file=resume_file,
                job_role=job_role
            )
            
            # Analyze resume
            analysis = analyze_resume(resume.file.path, job_role)
            resume.analysis = analysis
            resume.save()
            
            return redirect('view_analysis', pk=resume.pk)
            
    return render(request, 'resume_analyzer/upload.html')

@login_required(login_url='signin')
def view_analysis(request, pk):
    resume = Resume.objects.get(pk=pk)
    return render(request, 'resume_analyzer/analysis.html', {'resume': resume})



def sign_up(request):
    if request.user.is_authenticated:
        return redirect('upload_resume')
        
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            try:
                user = form.save()
                login(request, user)
                messages.success(request, 'Account created successfully!')
                return redirect('upload_resume')
            except Exception as e:
                messages.error(request, 'Error creating account. Please try again.')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{error}')
    else:
        form = SignUpForm()
    
    return render(request, 'resume_analyzer/signup.html', {'form': form})

def sign_in(request):
    if request.user.is_authenticated:
        return redirect('upload_resume')
        
    if request.method == 'POST':
        form = SignInForm(request, data=request.POST)
        if form.is_valid():
            try:
                user = form.get_user()
                login(request, user)
                messages.success(request, 'Logged in successfully!')
                
                # Check for next parameter
                next_url = request.GET.get('next')
                if next_url:
                    return redirect(next_url)
                return redirect('upload_resume')
            except Exception as e:
                messages.error(request, 'Error logging in. Please try again.')
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = SignInForm()
    
    return render(request, 'resume_analyzer/signin.html', {'form': form})

@login_required
def log_out(request):
    try:
        logout(request)
        messages.success(request, 'Logged out successfully!')
    except Exception as e:
        messages.error(request, 'Error logging out. Please try again.')
    return redirect('upload_resume')