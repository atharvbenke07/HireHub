from django.urls import path

from .views import (
    JobListView,
    JobDetailView,
    JobCreateView,
    JobUpdateView,
    JobDeleteView,
)


urlpatterns = [

    path(
        'jobs/',
        JobListView.as_view(),
        name='job_list'
    ),

    path(
        'jobs/create/',
        JobCreateView.as_view(),
        name='job_create'
    ),

    path(
        'jobs/<int:pk>/',
        JobDetailView.as_view(),
        name='job_detail'
    ),

    path(
        'jobs/<int:pk>/edit/',
        JobUpdateView.as_view(),
        name='job_update'
    ),

    path(
        'jobs/<int:pk>/delete/',
        JobDeleteView.as_view(),
        name='job_delete'
    ),
]