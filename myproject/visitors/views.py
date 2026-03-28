from django.shortcuts import render
from myapp.models import Course

def dashboard(request):
    courses = Course.objects.all()[:6]

    return render(request, 'visitors/dashboard.html', {
        "courses": courses
    })