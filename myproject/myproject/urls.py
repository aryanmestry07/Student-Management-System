from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', include('accounts.urls', namespace='accounts')),

    # 🌐 WEBSITE (HOME PAGE)
    path('', include('visitors.urls', namespace='visitors')),

    path('admin-panel/', include('myapp.urls', namespace='myapp')),

    # 👨‍🎓 Student panel
    path('student/', include('student.urls', namespace='student')),

    # 🔐 Accounts
    path('accounts/', include('accounts.urls', namespace='accounts')),

    # 🤖 Chatbot
    path('chatbot/', include('chatbot.urls')),
]