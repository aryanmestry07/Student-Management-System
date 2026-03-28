# myproject/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    # Main site
     path('', include('myapp.urls', namespace='myapp')),

    # Accounts
    path('accounts/', include('accounts.urls', namespace='accounts')),  # auth
   

    # Student panel
    path('student/', include('student.urls', namespace='student')),

    #Visitors sites
    path('', include('visitors.urls', namespace='visitors')),

    path('chatbot/', include('chatbot.urls')),
]

