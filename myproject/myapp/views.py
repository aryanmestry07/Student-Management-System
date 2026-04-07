#myapp/views.py
import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth import update_session_auth_hash
from django.db.models import Count
from django.db.models.functions import ExtractMonth
from django.db.models import Q

from .models import Course, Topic, Assignment,Quiz, Question,Notice

from student.models import Student
from .forms import (
    CourseForm, StudentForm, StudentUpdateForm, UserUpdateForm,
    TopicForm, AssignmentForm, QuizForm,NoticeForm
)
from student.forms import StudentSignupForm  # ✅ import your existing form
from student.models import Student  # ✅ make sure to import Student model
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect


# ------------------ Dashboard ------------------
@login_required
def dashboard(request):
    total_students = Student.objects.count()
    total_courses = Course.objects.count()

    # Courses by category
    course_data = (
        Course.objects.values("category")
        .annotate(count=Count("id"))
        .order_by("category")
    )
    categories = [c["category"] for c in course_data]
    course_counts = [c["count"] for c in course_data]

    # Student enrollments over time
    enrollment_data = (
        Student.objects.annotate(month=ExtractMonth("enrollment_date"))
        .values("month")
        .annotate(count=Count("id"))
        .order_by("month")
    )
    enrollment_months = [e["month"] for e in enrollment_data]
    enrollment_counts = [e["count"] for e in enrollment_data]

    context = {
        "total_students": total_students,
        "total_courses": total_courses,
        "categories": json.dumps(categories),
        "course_counts": json.dumps(course_counts),
        "enrollment_months": json.dumps(enrollment_months),
        "enrollment_counts": json.dumps(enrollment_counts),
    }
    return render(request, "myapp/dashboard.html", context)

# ------------------ Student Views ------------------
@login_required
@login_required
def students_view(request):
    query = request.GET.get('q')

    students = Student.objects.select_related("user").all()

    if query:
        students = students.filter(
            Q(user__first_name__icontains=query) |
            Q(middle_name__icontains=query) |
            Q(last_name__icontains=query) |
            Q(user__email__icontains=query) |
            Q(user__username__icontains=query)
        )

    return render(request, "myapp/students.html", {
        "students": students,
        "query": query
    })
@login_required
def student_detail(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    return render(request, "myapp/student_detail.html", {"student": student})

@login_required

def student_signup_admin(request):
    if request.method == "POST":
        form = StudentSignupForm(request.POST)
        if form.is_valid():
            # User fields
            username = form.cleaned_data["username"]
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            first_name = form.cleaned_data["first_name"]

            # Check if username already exists
            if User.objects.filter(username=username).exists():
                messages.error(request, "Username already taken.")
                return redirect("myapp:student_signup_admin")

            # Create User
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=first_name,
            )

            # Create Student profile
            student = form.save(commit=False)
            student.user = user
            student.save()

            messages.success(request, "Student created successfully! ✅")
            return redirect("myapp:students")  # redirect to student list
    else:
        form = StudentSignupForm()

    return render(request, "myapp/add_student.html", {"form": form})

@login_required
def update_student(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    if request.method == "POST":
        student_form = StudentUpdateForm(request.POST, instance=student)
        user_form = UserUpdateForm(request.POST, instance=student.user)
        if student_form.is_valid() and user_form.is_valid():
            student_form.save()
            user_form.save()
            messages.success(request, "Student updated successfully! ✏️")
            return redirect("students")
    else:
        student_form = StudentUpdateForm(instance=student)
        user_form = UserUpdateForm(instance=student.user)
    return render(request, "myapp/update_student.html", {
        "student_form": student_form,
        "user_form": user_form,
        "student": student,
    })

@login_required
def edit_student(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    return redirect("update_student", student_id=student.id)

@login_required
def delete_student(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    user = student.user
    student.delete()
    user.delete()
    messages.success(request, "Student deleted successfully 🗑️")
    return redirect("students")

@login_required
def reset_student_password(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    user = student.user
    if request.method == "POST":
        form = SetPasswordForm(user, request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, user)
            messages.success(request, "Password reset successfully 🔑")
            return redirect("student_detail", student_id=student.id)
    else:
        form = SetPasswordForm(user)
    return render(request, "myapp/reset_password.html", {"form": form, "student": student})

@login_required
def add_course_to_student(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    if request.method == "POST":
        course_id = request.POST.get("course_id")
        if course_id:
            course = get_object_or_404(Course, id=course_id)
            student.courses.add(course)
            messages.success(request, f"Course '{course.name}' added to {student.user.username} ✅")
            return redirect("myapp:student_detail", student_id=student.id)
    courses = Course.objects.all()
    return render(request, "myapp/add_course_to_student.html", {"student": student, "courses": courses})

# ------------------ Course Views ------------------
@login_required
def course_list(request):
    courses = Course.objects.all()
    return render(request, "myapp/courses.html", {"courses": courses})

@login_required
def add_course(request):
    if request.method == "POST":
        form = CourseForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Course added successfully ✅")
            return redirect("myapp:courses")
    else:
        form = CourseForm()
    return render(request, "myapp/add_course.html", {"form": form})

@login_required
def edit_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    if request.method == "POST":
        form = CourseForm(request.POST, instance=course)
        if form.is_valid():
            form.save()
            messages.success(request, "Course updated successfully ✏️")
            return redirect("myapp:courses")
    else:
        form = CourseForm(instance=course)
    return render(request, "myapp/edit_course.html", {"form": form, "course": course})

@login_required
def delete_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    if request.method == "POST":
        course.delete()
        messages.success(request, "Course deleted successfully 🗑️")
        return redirect("myapp:courses")
    return render(request, "myapp/delete_course.html", {"course": course})

@login_required
def course_detail(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    students = course.enrolled_students.all()
    topics = course.topics.all()
    assignments = course.assignments.all()
    quizzes = course.quizzes.all()

    assignment_form = AssignmentForm()
    quiz_form = QuizForm()

    context = {
        "course": course,
        "students": students,
        "topics": topics,
        "assignments": assignments,
        "quizzes": quizzes,
        "assignment_form": assignment_form,
        "quiz_form": quiz_form,
    }
    return render(request, "myapp/course_detail.html", context)

# ------------------ Topic Views ------------------
@login_required
def view_topics(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    topics = course.topics.all()
    return render(request, "myapp/view_topics.html", {"course": course, "topics": topics})

@login_required
def add_topic(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    if request.method == 'POST':
        form = TopicForm(request.POST, request.FILES)
        if form.is_valid():
            topic = form.save(commit=False)
            topic.course = course
            topic.save()
            return redirect('myapp:course_detail', course_id=course.id)
    else:
        form = TopicForm()
    return render(request, 'myapp/add_topic.html', {'form': form, 'course': course})

@login_required
def topic_detail(request, topic_id):
    topic = get_object_or_404(Topic, id=topic_id)
    # Get quizzes that have at least one question in this topic
    quizzes = topic.course.quizzes.filter(questions__topic=topic).distinct()

    return render(request, "myapp/topic_detail.html", {
        "topic": topic,
        "quizzes": quizzes,
    })

@login_required
def edit_topic(request, topic_id):
    topic = get_object_or_404(Topic, id=topic_id)
    if request.method == "POST":
        form = TopicForm(request.POST, request.FILES, instance=topic)
        if form.is_valid():
            form.save()
            return redirect("myapp:course_detail", course_id=topic.course.id)
    else:
        form = TopicForm(instance=topic)
    return render(request, "myapp/edit_topic.html", {"form": form, "topic": topic})

@login_required
def delete_topic(request, topic_id):
    topic = get_object_or_404(Topic, id=topic_id)
    course_id = topic.course.id
    topic.delete()
    return redirect("myapp:course_detail", course_id=course_id)

@login_required
def topic_assignments(request, topic_id):
    topic = get_object_or_404(Topic, id=topic_id)
    assignments = topic.assignments.all()  # if Assignment has ForeignKey to Topic
    return render(request, 'student/topic_assignments.html', {
        'topic': topic,
        'assignments': assignments
    })

# ------------------ Assignment Views ------------------
@login_required
def add_assignment(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    if request.method == "POST":
        form = AssignmentForm(request.POST)
        if form.is_valid():
            assignment = form.save(commit=False)
            assignment.course = course
            assignment.save()
            messages.success(request, "Assignment added successfully ✅")
            return redirect("myapp:course_detail", course_id=course.id)
    else:
        form = AssignmentForm()
    return render(request, "myapp/add_assignment.html", {"form": form, "course": course})

@login_required
def edit_assignment(request, course_id, assignment_id):
    course = get_object_or_404(Course, id=course_id)
    assignment = get_object_or_404(Assignment, id=assignment_id, course=course)
    if request.method == "POST":
        form = AssignmentForm(request.POST, instance=assignment)
        if form.is_valid():
            form.save()
            messages.success(request, "Assignment updated successfully ✏️")
            return redirect("myapp:course_detail", course_id=course.id)
    else:
        form = AssignmentForm(instance=assignment)
    return render(request, "myapp/edit_assignment.html", {
        "form": form,
        "course": course,
        "assignment": assignment,
    })

@login_required
def delete_assignment(request, course_id, assignment_id):
    course = get_object_or_404(Course, id=course_id)
    assignment = get_object_or_404(Assignment, id=assignment_id, course=course)
    if request.method == "POST":
        assignment.delete()
        messages.success(request, "Assignment deleted successfully 🗑️")
        return redirect("myapp:course_detail", course_id=course.id)
    return render(request, "myapp/delete_assignment.html", {
        "course": course,
        "assignment": assignment,
    })

# ------------------ Quiz Views ------------------
# ------------------ Quiz Views (Updated) ------------------
@login_required
def add_quiz(request, course_id, topic_id):
    course = get_object_or_404(Course, id=course_id)
    topic = get_object_or_404(Topic, id=topic_id, course=course)

    if request.method == "POST":
        # Create quiz tied to the topic
        quiz = Quiz.objects.create(
            course=course,
            topic=topic,
            title=request.POST.get("quiz_title", "Untitled Quiz"),
            description=request.POST.get("quiz_description", "")
        )

        # Loop through form inputs for questions
        correct_map = {"1": "A", "2": "B", "3": "C", "4": "D"}
        for i in range(1, 51):  # Max 50 questions
            question_text = request.POST.get(f"question_{i}")
            if question_text:
                Question.objects.create(
                    quiz=quiz,
                    topic=topic,  # ✅ Assign topic
                    text=question_text,
                    option_a=request.POST.get(f"option1_{i}"),
                    option_b=request.POST.get(f"option2_{i}"),
                    option_c=request.POST.get(f"option3_{i}"),
                    option_d=request.POST.get(f"option4_{i}"),
                    correct_answer=correct_map.get(request.POST.get(f"correct_{i}"))
                )

        messages.success(request, "Quiz created successfully ✅")
        return redirect("myapp:topic_detail", topic_id=topic.id)

    return render(request, "myapp/add_quiz.html", {
        "course": course,
        "topic": topic,
        "questions_range": range(1, 3),  # Show 2 questions by default
    })


@login_required
def view_quiz(request, course_id, quiz_id):
    """Show quiz questions for a specific quiz and its topic."""
    course = get_object_or_404(Course, id=course_id)
    quiz = get_object_or_404(Quiz, id=quiz_id, course=course)

    # Show questions tied to the quiz's topic
    questions = quiz.questions.filter(topic=quiz.topic) if quiz.topic else quiz.questions.all()

    return render(request, "myapp/view_quiz.html", {
        "course": course,
        "quiz": quiz,
        "questions": questions,
    })



@login_required
def edit_quiz(request, course_id, quiz_id):
    course = get_object_or_404(Course, id=course_id)
    quiz = get_object_or_404(Quiz, id=quiz_id, course=course)

    correct_map = {"1": "A", "2": "B", "3": "C", "4": "D"}

    if request.method == "POST":
        form = QuizForm(request.POST, instance=quiz)
        if form.is_valid():
            form.save()

            for question in quiz.questions.all():
                question.text = request.POST.get(f"question_{question.id}", question.text)
                question.option_a = request.POST.get(f"option1_{question.id}", question.option_a)
                question.option_b = request.POST.get(f"option2_{question.id}", question.option_b)
                question.option_c = request.POST.get(f"option3_{question.id}", question.option_c)
                question.option_d = request.POST.get(f"option4_{question.id}", question.option_d)
                correct_raw = request.POST.get(f"correct_{question.id}")
                if correct_raw:
                    question.correct_answer = correct_map.get(correct_raw, question.correct_answer)
                question.save()

            messages.success(request, "Quiz updated successfully ✏️")
            return redirect("myapp:course_detail", course_id=course.id)
    else:
        form = QuizForm(instance=quiz)

    return render(request, "myapp/edit_quiz.html", {
        "form": form,
        "course": course,
        "quiz": quiz,
        "questions": quiz.questions.all(),
    })



@login_required
def delete_quiz(request, course_id, quiz_id):
    course = get_object_or_404(Course, id=course_id)
    quiz = get_object_or_404(Quiz, id=quiz_id, course=course)

    if request.method == "POST":
        quiz_title = quiz.title
        quiz.delete()
        messages.success(request, f"Quiz '{quiz_title}' deleted successfully 🗑️")
        return redirect("myapp:course_detail", course_id=course.id)

    return render(request, "myapp/delete_quiz.html", {
        "course": course,
        "quiz": quiz,
    })


def notice_list(request):
    notices = Notice.objects.filter(is_active=True).order_by('-created_at')
    return render(request, 'myapp/notice_list.html', {'notices': notices})

def add_notice(request):
    if request.method == 'POST':
        form = NoticeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('myapp:notice_list')
    else:
        form = NoticeForm()
    return render(request, 'myapp/add_notice.html', {'form': form})


def edit_notice(request, notice_id):
    notice = get_object_or_404(Notice, id=notice_id)

    if request.method == 'POST':
        form = NoticeForm(request.POST, instance=notice)
        if form.is_valid():
            form.save()
            return redirect('myapp:notice_list')
    else:
        form = NoticeForm(instance=notice)

    return render(request, 'myapp/edit_notice.html', {'form': form})


def delete_notice(request, notice_id):
    notice = get_object_or_404(Notice, id=notice_id)

    if request.method == 'POST':
        notice.delete()
        return redirect('myapp:notice_list')

    return render(request, 'myapp/delete_notice.html', {'notice': notice})

