from django.shortcuts import render
from myapp.models import Course

def dashboard(request):
    courses = Course.objects.all()[:6]

    return render(request, 'visitors/dashboard.html', {
        "courses": courses
    })




def all_courses(request):
    courses = Course.objects.all().order_by("-id")  # latest first
    return render(request, "visitors/all_courses.html", {"courses": courses})




from django.shortcuts import redirect
from .models import ContactMessage  # we will create this later

def contact_submit(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        subject = request.POST.get("subject")
        message = request.POST.get("message")

        ContactMessage.objects.create(
            name=name,
            email=email,
            subject=subject,
            message=message
        )

        return redirect("/")  # back to homepage