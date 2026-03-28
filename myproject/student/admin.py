# student/admin.py
from django.contrib import admin
from .models import Student

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone', 'enrollment_date')
    search_fields = ('user__username', 'user__first_name', 'user__last_name', 'phone')
    list_filter = ('enrollment_date',)
    filter_horizontal = ('courses',)  # Nice UI for ManyToMany
