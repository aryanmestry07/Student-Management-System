from django.contrib import admin
from django.urls import path, include

# ✅ ADD THESE
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # 🔐 Custom Admin Login
    path('admin/', include('accounts.urls', namespace='accounts')),

    # 🔥 Admin Panel
    path('admin-panel/', include('myapp.urls', namespace='myapp')),

    # 🌐 Website
    path('', include('visitors.urls', namespace='visitors')),

    # 👨‍🎓 Student Panel
    path('student/', include('student.urls', namespace='student')),

    # 🤖 Chatbot
    path('chatbot/', include('chatbot.urls')),
]

# ✅ VERY IMPORTANT (for PDF/images)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)