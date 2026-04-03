#myapp/urls
from django.urls import path
from . import views

app_name = "myapp"

urlpatterns = [
    # Dashboard
    path('dashboard/', views.dashboard, name='dashboard'),



    # Students
    path('students/', views.students_view, name='students'),
    path("students/add/", views.student_signup_admin, name="student_signup_admin"),
    path('students/<int:student_id>/', views.student_detail, name='student_detail'),
    path('students/<int:student_id>/edit/', views.edit_student, name='edit_student'),
    path('students/<int:student_id>/update/', views.update_student, name='update_student'),
    path('students/<int:student_id>/delete/', views.delete_student, name='delete_student'),
    path('students/<int:student_id>/reset-password/', views.reset_student_password, name='reset_student_password'),
    path("students/<int:student_id>/add-course/", views.add_course_to_student, name="add_course_to_student"),

    # Courses
    path('courses/', views.course_list, name='courses'),
    path('courses/add/', views.add_course, name='add_course'),
    path('courses/<int:course_id>/', views.course_detail, name='course_detail'),
    path('courses/<int:course_id>/edit/', views.edit_course, name='edit_course'),
    path('courses/<int:course_id>/delete/', views.delete_course, name='delete_course'),

    # Topics
    path("courses/<int:course_id>/topics/", views.view_topics, name="view_topics"),
    path("courses/<int:course_id>/topic/add/", views.add_topic, name="add_topic"),
    path("topics/<int:topic_id>/edit/", views.edit_topic, name="edit_topic"),
    path("topics/<int:topic_id>/delete/", views.delete_topic, name="delete_topic"),
    path("topics/<int:topic_id>/assignments/", views.topic_assignments, name="topic_assignments"),
    path("topics/<int:topic_id>/", views.topic_detail, name="topic_detail"),

    # Assignments
    path("courses/<int:course_id>/assignment/add/", views.add_assignment, name="add_assignment"),
    path("courses/<int:course_id>/assignment/<int:assignment_id>/edit/", views.edit_assignment, name="edit_assignment"),
    path("courses/<int:course_id>/assignment/<int:assignment_id>/delete/", views.delete_assignment, name="delete_assignment"),

  # ----------------------------
# Quizzes
# ----------------------------
# Add Quiz (topic-specific)
# myapp/urls.py
path(
    'courses/<int:course_id>/quiz/add/<int:topic_id>/',
    views.add_quiz,
    name='add_quiz'
),

# Edit Quiz
path("courses/<int:course_id>/quiz/<int:quiz_id>/edit/", views.edit_quiz, name="edit_quiz"),

# Delete Quiz
path("courses/<int:course_id>/quiz/<int:quiz_id>/delete/", views.delete_quiz, name="delete_quiz"),

# View quiz detail
path("courses/<int:course_id>/quiz/<int:quiz_id>/", views.view_quiz, name="view_quiz"),

path('notices/', views.notice_list, name='notice_list'),
path('notices/add/', views.add_notice, name='add_notice'),

path('notices/edit/<int:notice_id>/', views.edit_notice, name='edit_notice'),
path('notices/delete/<int:notice_id>/', views.delete_notice, name='delete_notice'),


]
