from django.db import models
from django.contrib.auth.models import User

from jobs.models import Job


class Application(models.Model):

    STATUS_CHOICES = (
        ('Applied', 'Applied'),
        ('Shortlisted', 'Shortlisted'),
        ('Rejected', 'Rejected'),
        ('Selected', 'Selected'),
    )

    job = models.ForeignKey(
        Job,
        on_delete=models.CASCADE,
        related_name='applications'
    )

    applicant = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='applications'
    )

    resume = models.FileField(
        upload_to='resumes/',
        blank=True,
        null=True
    )

    cover_letter = models.TextField()

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='Applied'
    )

    applied_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return f'{self.applicant.username} - {self.job.title}'

class Meta:

    constraints = [
        models.UniqueConstraint(
            fields=['job', 'applicant'],
            name='unique_job_application'
        )
    ]

def __str__(self):
    return f'{self.applicant.username} - {self.job.title}'