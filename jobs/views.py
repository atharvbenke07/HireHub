from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.template import context
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from django.urls import reverse_lazy

from .models import Job, Category
from .forms import JobForm


# =========================================================
# JOB LIST
# =========================================================

class JobListView(ListView):

    model = Job
    template_name = 'jobs/job_list.html'
    context_object_name = 'jobs'
    paginate_by = 10

    def get_queryset(self):

        queryset = Job.objects.filter(
            is_active=True
        ).select_related(
            'company',
            'category'
        ).order_by(
            '-created_at'
        )

        keyword = self.request.GET.get('keyword')

        if keyword:
            queryset = queryset.filter(
                Q(title__icontains=keyword)
                | Q(description__icontains=keyword)
                | Q(skills__icontains=keyword)
            )

        # Location search
        location = self.request.GET.get('location')

        if location:
            queryset = queryset.filter(
                location__icontains=location
           )

        #Job type search
        job_type = self.request.GET.get(
            'job_type'
        )

        if job_type:
            queryset = queryset.filter(
                job_type=job_type
            )

        #Add Experience search
        experience = self.request.GET.get(
            'experience'
            )

        if experience:
            queryset = queryset.filter(
                experience__icontains=experience
            )

        #Add catagory search
        category = self.request.GET.get(
            'category'
            )

        if category:
            queryset = queryset.filter(
                category_id=category
            )

        #Add minimum salary search
        salary_min = self.request.GET.get(
            'salary_min'
            )

        if salary_min:
            queryset = queryset.filter(
                salary_min__gte=salary_min
            )

        #Add maximum salary search
        salary_max = self.request.GET.get(
            'salary_max'
            )

        if salary_max:
            queryset = queryset.filter(
                salary_max__lte=salary_max
            )

        return queryset

    def get_context_data(
        self,
        **kwargs
    ):

        context = super().get_context_data(
            **kwargs
       )

        context['categories'] = (
            Category.objects.all()
        )

        context['job_types'] = [
            choice[0]
            for choice in Job.JOB_TYPE_CHOICES
        ]

        return context 


# =========================================================
# JOB DETAIL
# =========================================================

class JobDetailView(DetailView):

    model = Job
    template_name = 'jobs/job_detail.html'
    context_object_name = 'job'


# =========================================================
# JOB CREATE
# =========================================================

class JobCreateView(
    LoginRequiredMixin,
    CreateView
):

    model = Job
    form_class = JobForm
    template_name = 'jobs/job_form.html'
    success_url = reverse_lazy('job_list')

    def dispatch(self, request, *args, **kwargs):

        if request.user.profile.user_type != 'recruiter':

            messages.error(
                request,
                'Only recruiters can create jobs.'
            )

            return redirect('job_list')

        # Check company
        if not hasattr(request.user, 'company'):

            messages.error(
                request,
                'Please create your company before creating a job.'
            )

            return redirect('company_create')

        return super().dispatch(
            request,
            *args,
            **kwargs
        )

    def form_valid(self, form):

        company = self.request.user.company

        form.instance.company = company

        messages.success(
            self.request,
            'Job created successfully.'
        )

        return super().form_valid(form)


# =========================================================
# JOB UPDATE
# =========================================================

class JobUpdateView(
    LoginRequiredMixin,
    UpdateView
):

    model = Job
    form_class = JobForm
    template_name = 'jobs/job_form.html'
    success_url = reverse_lazy('job_list')

    def dispatch(self, request, *args, **kwargs):

        job = self.get_object()

        if request.user.profile.user_type != 'recruiter':

            messages.error(
                request,
                'Only recruiters can edit jobs.'
            )

            return redirect('job_list')

        if job.company.recruiter != request.user:

            messages.error(
                request,
                'You can only edit your own jobs.'
            )

            return redirect('job_list')

        return super().dispatch(
            request,
            *args,
            **kwargs
        )

    def form_valid(self, form):

        messages.success(
            self.request,
            'Job updated successfully.'
        )

        return super().form_valid(form)


# =========================================================
# JOB DELETE
# =========================================================

class JobDeleteView(
    LoginRequiredMixin,
    DeleteView
):

    model = Job
    template_name = 'jobs/job_confirm_delete.html'
    success_url = reverse_lazy('job_list')

    def dispatch(self, request, *args, **kwargs):

        job = self.get_object()

        if request.user.profile.user_type != 'recruiter':

            messages.error(
                request,
                'Only recruiters can delete jobs.'
            )

            return redirect('job_list')

        if job.company.recruiter != request.user:

            messages.error(
                request,
                'You can only delete your own jobs.'
            )

            return redirect('job_list')

        return super().dispatch(
            request,
            *args,
            **kwargs
        )

    def form_valid(self, form):

        messages.success(
            self.request,
            'Job deleted successfully.'
        )

        return super().form_valid(form)


# =========================================================
# HOME
# =========================================================

def home(request):

    return render(
        request,
        'home.html'
    )