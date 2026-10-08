from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse

from accounts.models import Profile
from companies.models import Company
from .models import Job, Category


class JobTests(TestCase):

    def setUp(self):

        self.user = User.objects.create_user(
            username="recruiter",
            email="recruiter@example.com",
            password="Test@123"
        )

        Profile.objects.create(
            user=self.user,
            user_type="recruiter"
        )

        self.company = Company.objects.create(
            recruiter=self.user,
            company_name="Test Company",
            description="Test Company",
            location="Pune"
        )

        self.category = Category.objects.create(
            name="IT",
            description="Information Technology"
        )

        self.job = Job.objects.create(
            company=self.company,
            category=self.category,
            title="Python Developer",
            description="Python Django Developer",
            location="Pune",
            salary_min=30000,
            salary_max=50000,
            experience="Fresher",
            job_type="Full Time",
            skills="Python, Django",
            deadline="2026-12-31",
            is_active=True
        )

    def test_job_list(self):

        response = self.client.get(
            reverse("job_list")
        )

        self.assertEqual(response.status_code, 200)

    def test_job_detail(self):

        response = self.client.get(
            reverse(
                "job_detail",
                kwargs={"pk": self.job.pk}
            )
        )

        self.assertEqual(response.status_code, 200)

    def test_job_title_exists(self):

        self.assertEqual(
            self.job.title,
            "Python Developer"
        )