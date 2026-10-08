from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Company
from .forms import CompanyForm


@login_required
def create_company(request):

    if request.user.profile.user_type != 'recruiter':
        messages.error(
            request,
            "Only recruiters can create a company."
        )

        return redirect('dashboard')

    if Company.objects.filter(
        recruiter=request.user
    ).exists():

        messages.warning(
            request,
            "You already have a company."
        )

        return redirect('company')

    if request.method == 'POST':

        form = CompanyForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():

            company = form.save(
                commit=False
            )

            company.recruiter = request.user

            company.save()

            messages.success(
                request,
                "Company created successfully."
            )

            return redirect('company')

    else:

        form = CompanyForm()

    return render(
        request,
        'companies/create_company.html',
        {
            'form': form
        }
    )

@login_required
def company_detail(request):

    company = Company.objects.filter(
        recruiter=request.user
    ).first()

    if not company:

        return redirect('create_company')

    return render(
        request,
        'companies/company.html',
        {
            'company': company
        }
    )

@login_required
def edit_company(request):

    company = Company.objects.filter(
        recruiter=request.user
    ).first()

    if not company:

        return redirect('create_company')

    if request.method == 'POST':

        form = CompanyForm(
            request.POST,
            request.FILES,
            instance=company
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Company updated successfully."
            )

            return redirect('company')

    else:

        form = CompanyForm(
            instance=company
        )

    return render(
        request,
        'companies/edit_company.html',
        {
            'form': form
        }
    )