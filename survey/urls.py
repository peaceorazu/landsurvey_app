from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing_page, name='landing'),
    path('form/', views.index, name='index'),
    path('input/', views.input_form, name='input_form'),
    path('summary/', views.summary, name='summary'),
]
