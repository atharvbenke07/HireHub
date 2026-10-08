from django.urls import path

from .views import (
    JobListCreateAPIView,
    JobDetailAPIView,
    CategoryListAPIView,
    CompanyListAPIView,
)


urlpatterns = [

    path(
        "jobs/",
        JobListCreateAPIView.as_view(),
        name="api-job-list"
    ),

    path(
        "jobs/<int:pk>/",
        JobDetailAPIView.as_view(),
        name="api-job-detail"
    ),

    path(
        "categories/",
        CategoryListAPIView.as_view(),
        name="api-category-list"
    ),

    path(
        "companies/",
        CompanyListAPIView.as_view(),
        name="api-company-list"
    ),
]