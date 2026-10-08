from django.urls import path

from .views import (
    create_company,
    company_detail,
    edit_company
)


urlpatterns = [

    path(
        'company/create/',
        create_company,
        name='create_company'
    ),

    path(
        'company/',
        company_detail,
        name='company'
    ),

    path(
        'company/edit/',
        edit_company,
        name='edit_company'
    ),

]