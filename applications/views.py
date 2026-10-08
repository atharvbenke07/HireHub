from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import (
    render,
    redirect,
    get_object_or_404,
)

from jobs.models import Job

from .models import Application
from .forms import ApplicationForm, ApplicationStatusForm

@login_required
def apply_job(request, pk):

    job = get_object_or_404(
        Job,
        pk=pk,
        is_active=True
    )

    # Only Job Seekers can apply
    if request.user.profile.user_type != 'job_seeker':

        messages.error(
            request,
            'Only job seekers can apply for jobs.'
        )

        return redirect(
            'job_detail',
            pk=job.pk
        )

    if request.method == "POST":

        # Save application
        Application.objects.create(
            job=job,
            applicant=request.user,
            resume=request.FILES.get('resume'),
            cover_letter=request.POST.get('cover_letter')
        )

        messages.success(
            request,
            "Application submitted successfully."
        )

    # Check whether user already applied
    already_applied = Application.objects.filter(
        job=job,
        applicant=request.user
    ).exists()

    if already_applied:

        messages.warning(
            request,
            "You have already applied for this job."
        )

        return redirect(
            'job_detail',
            pk=job.pk
        )



    # Prevent duplicate application
    if Application.objects.filter(
        job=job,
        applicant=request.user
    ).exists():

        messages.warning(
            request,
            'You have already applied for this job.'
        )

        return redirect(
            'job_detail',
            pk=job.pk
        )

    if request.method == 'POST':

        form = ApplicationForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():

            application = form.save(
                commit=False
            )

            application.job = job
            application.applicant = request.user

            application.save()

            messages.success(
                request,
                'Application submitted successfully.'
            )

            return redirect(
                'my_applications'
            )

    else:

        form = ApplicationForm()

    return render(
        request,
        'applications/apply.html',
        {
            'form': form,
            'job': job,
        }
    )

@login_required
def my_applications(request):

    if request.user.profile.user_type != 'job_seeker':

        messages.error(
            request,
            'Only job seekers can view applications.'
        )

        return redirect('dashboard')

    applications = Application.objects.filter(
        applicant=request.user
    ).select_related(
        'job',
        'job__company',
        'job__category'
    ).order_by(
        '-applied_at'
    )

    return render(
        request,
        'applications/my_applications.html',
        {
            'applications': applications
        }
    )

@login_required
def recruiter_applicants(request):

    if request.user.profile.user_type != 'recruiter':

        messages.error(
            request,
            'Only recruiters can view applicants.'
        )

        return redirect('dashboard')

    applications = Application.objects.filter(
        job__company__recruiter=request.user
    ).select_related(
        'applicant',
        'applicant__profile',
        'job',
        'job__company'
    ).order_by(
        '-applied_at'
    )

    return render(
        request,
        'applications/recruiter_applicants.html',
        {
            'applications': applications
        }
    )

@login_required
def update_application_status(
    request,
    pk
):

    if request.user.profile.user_type != 'recruiter':

        messages.error(
            request,
            'Only recruiters can update application status.'
        )

        return redirect('dashboard')

    application = get_object_or_404(
        Application,
        pk=pk,
        job__company__recruiter=request.user
    )

    if request.method == 'POST':

        form = ApplicationStatusForm(
            request.POST,
            instance=application
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                'Application status updated successfully.'
            )

            return redirect(
                'recruiter_applicants'
            )

    else:

        form = ApplicationStatusForm(
            instance=application
        )

    return render(
        request,
        'applications/update_status.html',
        {
            'form': form,
            'application': application,
        }
    )