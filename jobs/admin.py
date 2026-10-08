from django.contrib import admin

from .models import Category, Job


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'name',
    )

    search_fields = (
        'name',
    )


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'title',
        'company',
        'category',
        'job_type',
        'location',
        'salary_min',
        'salary_max',
        'deadline',
        'is_active',
    )

    list_filter = (
        'job_type',
        'category',
        'is_active',
    )

    search_fields = (
        'title',
        'description',
        'skills',
        'location',
    )