from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from applications.models import Application
from jobs.models import Job

from .forms import ProfileForm, RegisterForm
from .models import Profile


# ============================================================
# REGISTER
# ============================================================

def register(request):

    if request.method == 'POST':

        form = RegisterForm(request.POST)

        if form.is_valid():

            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user_type = form.cleaned_data['user_type']

            # Check username
            if User.objects.filter(
                username=username
            ).exists():

                messages.error(
                    request,
                    "Username already exists."
                )

                return redirect('register')

            # Check email
            if User.objects.filter(
                email=email
            ).exists():

                messages.error(
                    request,
                    "Email already exists."
                )

                return redirect('register')

            # Create user
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password
            )

            # Create profile
            Profile.objects.create(
                user=user,
                user_type=user_type
            )

            messages.success(
                request,
                "Registration successful. Please login."
            )

            return redirect('login')

    else:

        form = RegisterForm()

    return render(
        request,
        'accounts/register.html',
        {
            'form': form
        }
    )


# ============================================================
# LOGIN
# ============================================================

def user_login(request):

    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            login(request, user)

            return redirect('dashboard')

        else:

            messages.error(
                request,
                "Invalid username or password."
            )

    return render(
        request,
        'accounts/login.html'
    )


# ============================================================
# DASHBOARD
# ============================================================

@login_required
def dashboard(request):

    user = request.user

    # ========================================================
    # JOB SEEKER DASHBOARD
    # ========================================================

    if user.profile.user_type == 'job_seeker':

        applications = Application.objects.filter(
            applicant=user
        ).select_related(
            'job',
            'job__company'
        ).order_by(
            '-applied_at'
        )

        context = {

            'total_applications':
                applications.count(),

            'applied':
                applications.filter(
                    status='Applied'
                ).count(),

            'shortlisted':
                applications.filter(
                    status='Shortlisted'
                ).count(),

            'selected':
                applications.filter(
                    status='Selected'
                ).count(),

            'rejected':
                applications.filter(
                    status='Rejected'
                ).count(),

            'recent_applications':
                applications[:5],
        }

        return render(
            request,
            'accounts/job_seeker_dashboard.html',
            context
        )


    # ========================================================
    # RECRUITER DASHBOARD
    # ========================================================

    elif user.profile.user_type == 'recruiter':

        jobs = Job.objects.filter(
            company__recruiter=user
        )

        applications = Application.objects.filter(
            job__company__recruiter=user
        ).select_related(
            'job',
            'applicant'
        ).order_by(
            '-applied_at'
        )

        context = {

            'total_jobs':
                jobs.count(),

            'active_jobs':
                jobs.filter(
                    is_active=True
                ).count(),

            'total_applicants':
                applications.count(),

            'shortlisted':
                applications.filter(
                    status='Shortlisted'
                ).count(),

            'selected':
                applications.filter(
                    status='Selected'
                ).count(),

            'recent_applications':
                applications[:5],
        }

        return render(
            request,
            'accounts/recruiter_dashboard.html',
            context
        )


    # ========================================================
    # DEFAULT DASHBOARD
    # ========================================================

    return render(
        request,
        'accounts/dashboard.html'
    )


# ============================================================
# LOGOUT
# ============================================================

def user_logout(request):

    logout(request)

    messages.success(
        request,
        "You have been logged out."
    )

    return redirect('login')


# ============================================================
# PROFILE
# ============================================================

@login_required
def profile(request):

    user_profile = request.user.profile

    return render(
        request,
        'accounts/profile.html',
        {
            'profile': user_profile
        }
    )


# ============================================================
# EDIT PROFILE
# ============================================================

@login_required
def edit_profile(request):

    user_profile = request.user.profile

    if request.method == 'POST':

        form = ProfileForm(
            request.POST,
            request.FILES,
            instance=user_profile
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Profile updated successfully."
            )

            return redirect('profile')

    else:

        form = ProfileForm(
            instance=user_profile
        )

    return render(
        request,
        'accounts/edit_profile.html',
        {
            'form': form
        }
    )