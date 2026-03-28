from django.urls import path
from . import views

app_name = 'visitors' 

urlpatterns = [
    # The dashboard is the only page now
    path('ice/', views.dashboard, name='dashboard'), 
    
    # We remove the /about/ and /contact/ paths
]