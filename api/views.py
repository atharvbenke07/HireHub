from rest_framework import generics

from jobs.models import Job, Category
from companies.models import Company

from .serializers import (
    JobSerializer,
    CategorySerializer,
    CompanySerializer,
)

class JobListCreateAPIView(generics.ListCreateAPIView):

    queryset = Job.objects.select_related(
        "company",
        "category"
    ).all()

    serializer_class = JobSerializer

class JobDetailAPIView(generics.RetrieveUpdateDestroyAPIView):

    queryset = Job.objects.select_related(
        "company",
        "category"
    ).all()

    serializer_class = JobSerializer

class CategoryListAPIView(generics.ListAPIView):

    queryset = Category.objects.all()

    serializer_class = CategorySerializer

class CompanyListAPIView(generics.ListAPIView):

    queryset = Company.objects.all()

    serializer_class = CompanySerializer