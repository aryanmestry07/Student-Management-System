from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy

def student_login_required(view_func):
    return login_required(
        view_func,
        login_url=reverse_lazy('student:student_login')  # Reverse from URL name
    )
