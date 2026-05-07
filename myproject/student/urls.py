from django.urls import path
from . import views

app_name = 'student'   # ✅ FIXED

urlpatterns = [
    # Home & Auth
    path('', views.student_home, name='student_home'),
    path('dashboard/', views.student_dashboard, name='student_dashboard'),
    path('login/', views.student_login, name='student_login'),
    path('logout/', views.student_logout, name='student_logout'),

    # Enrollment
    path('enroll/<int:course_id>/', views.enroll_in_course, name='enroll_in_course'),
    path('my-courses/', views.my_courses, name='my_courses'),

    # Courses
    path('course/<int:course_id>/', views.course_detail, name='course_detail'),
    path('course/<int:course_id>/topics/', views.course_topics, name='course_topics'),
    path('course/<int:course_id>/assignments/', views.course_assignments, name='course_assignments'),

    # Topics
    path("topics/<int:topic_id>/", views.topic_detail, name="topic_detail"),
    path("quiz/<int:quiz_id>/take/", views.take_quiz, name="take_quiz"),
    path('topic/<int:topic_id>/assignments/', views.topic_assignments, name='topic_assignments'),

    # ✅ ATTENDANCE (CORRECT)
    path('topic/<int:topic_id>/attendance/', views.mark_attendance, name='mark_attendance'),

    # Assignments & Submissions
    path('assignment/<int:assignment_id>/submit/', views.submit_assignment, name='submit_assignment'),
    path("assignments/", views.all_assignments, name="all_assignments"),

    path('notices/', views.notice_board, name='notice_board'),
    path('id-card/', views.id_card, name='id_card'),

    # ✅ FINAL EXAM
    path('course/<int:course_id>/start-exam/', views.start_exam, name='start_exam'),
    path('course/<int:course_id>/exam-result/', views.exam_result, name='exam_result'),
    path('certificate/<int:student_id>/<int:course_id>/',
     views.generate_certificate_view,
     name='generate_certificate'),

    path('my-certificates/', views.my_certificates, name='my_certificates'),
    path('verify-certificate/', views.verify_certificate, name='verify_certificate'),
]