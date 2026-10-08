from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse

from accounts.models import Profile
from companies.models import Company
from jobs.models import Job, Category
from .models import Application


class ApplicationTests(TestCase):

    def setUp(self):

        # Recruiter
        self.recruiter = User.objects.create_user(
            username="recruiter",
            email="recruiter@example.com",
            password="Test@123"
        )

        Profile.objects.create(
            user=self.recruiter,
            user_type="recruiter"
        )

        # Company
        self.company = Company.objects.create(
            recruiter=self.recruiter,
            company_name="Test Company",
            description="Test Company",
            location="Pune"
        )

        # Category
        self.category = Category.objects.create(
            name="IT",
            description="Information Technology"
        )

        # Job
        self.job = Job.objects.create(
            company=self.company,
            category=self.category,
            title="Python Developer",
            description="Python Developer",
            location="Pune",
            salary_min=30000,
            salary_max=50000,
            experience="Fresher",
            job_type="Full Time",
            skills="Python, Django",
            deadline="2026-12-31",
            is_active=True
        )

        # Job seeker
        self.seeker = User.objects.create_user(
            username="seeker",
            email="seeker@example.com",
            password="Test@123"
        )

        Profile.objects.create(
            user=self.seeker,
            user_type="job_seeker"
        )

    def test_application_creation(self):

        application = Application.objects.create(
            job=self.job,
            applicant=self.seeker,
            cover_letter="I am interested in this job."
        )

        self.assertEqual(
            application.status,
            "Applied"
        )

    def test_application_count(self):

        Application.objects.create(
            job=self.job,
            applicant=self.seeker,
            cover_letter="I am interested."
        )

        self.assertEqual(
            Application.objects.count(),
            1
        )