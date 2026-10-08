from rest_framework import serializers

from jobs.models import Job, Category
from companies.models import Company

class JobSerializer(serializers.ModelSerializer):

    company_name = serializers.CharField(
        source="company.company_name",
        read_only=True
    )

    category_name = serializers.CharField(
        source="category.name",
        read_only=True
    )

    class Meta:
        model = Job

        fields = [
            "id",
            "company",
            "company_name",
            "category",
            "category_name",
            "title",
            "description",
            "location",
            "salary_min",
            "salary_max",
            "experience",
            "job_type",
            "skills",
            "deadline",
            "is_active",
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "created_at",
            "updated_at",
        ]

class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category

        fields = [
            "id",
            "name",
            "description",
        ]

class CompanySerializer(serializers.ModelSerializer):

    class Meta:
        model = Company

        fields = [
            "id",
            "recruiter",
            "company_name",
            "description",
            "website",
            "location",
            "logo",
            "created_at",
        ]

        read_only_fields = [
            "created_at",
        ]