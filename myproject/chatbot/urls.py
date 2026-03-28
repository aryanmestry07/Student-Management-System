from django.urls import path
from . import views

# This 'app_name' is good practice
app_name = 'chatbot'

urlpatterns = [
    # This URL will be /chatbot/response/
    path('response/', views.chatbot_response, name='chatbot_response'),
]