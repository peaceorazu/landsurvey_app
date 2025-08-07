from django.urls import path
from .views import (
    landing_page,
    index,
    input_form,
    export_pdf,  # Import the class-based view
    summary
)

urlpatterns = [
    path('', landing_page, name='landing'),
    path('survey/', index, name='index'),
    path('survey/input/', input_form, name='input_form'),
    path('survey/export-pdf/', export_pdf, name='export_pdf'),
    path('survey/summary/', summary, name='summary'),
]