# myapp/admin.py
from django.contrib import admin
from .models import Course, Topic, Assignment,Notice


class TopicInline(admin.TabularInline):
    model = Topic
    extra = 1   # how many empty rows to show


class AssignmentInline(admin.TabularInline):
    model = Assignment
    extra = 1


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'duration', 'price')
    search_fields = ('name', 'category')
    inlines = [TopicInline, AssignmentInline]


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ('title', 'course')
    search_fields = ('title', 'course__name')


@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'due_date')
    search_fields = ('title', 'course__name')


@admin.register(Notice)
class NoticeAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at', 'is_active')
    search_fields = ('title',)