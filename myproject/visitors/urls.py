from django.urls import path
from . import views

app_name = 'visitors' 

urlpatterns = [
    path('', views.dashboard, name='dashboard'), 
    path("courses/", views.all_courses, name="all_courses"),
    path("contact-submit/", views.contact_submit, name="contact_submit"),
]