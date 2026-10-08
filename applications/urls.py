from django.urls import path

from .views import apply_job, my_applications, recruiter_applicants, update_application_status


urlpatterns = [

    path(
        'jobs/<int:pk>/apply/',
        apply_job,
        name='apply_job'
    ),


    path(
        'applications/',
        my_applications,
        name='my_applications'
    ),

    path(
        'recruiter/applicants/',
        recruiter_applicants,
        name='recruiter_applicants'
    ),

    path(
        'recruiter/applications/<int:pk>/status/',
        update_application_status,
        name='update_application_status'
   ),

]