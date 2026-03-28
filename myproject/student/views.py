from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.db.models import Q

from myapp.models import Course, Topic, Assignment, Quiz, Question, QuizSubmission
from .models import Student, Attendance, Submission
from .forms import StudentSignupForm, AssignmentUploadForm
from .decorators import student_login_required

from myapp.models import Notice
from django.utils.timezone import now



# ----------------------------
# HOME + AUTH
# ----------------------------
def student_home(request):
    return redirect("student:student_login")


def student_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect("student:student_dashboard")
        else:
            messages.error(request, "Invalid username or password")
            return render(request, "student/login.html", {"username": username})
    return render(request, "student/login.html")


@student_login_required
def student_dashboard(request):
    try:
        student = request.user.student_profile
    except Student.DoesNotExist:
        student = None

    assignments = Assignment.objects.filter(
        course__in=student.courses.all()
    ).order_by('-due_date')[:5]

    notices = Notice.objects.filter(
        is_active=True
    ).filter(
        Q(expiry_date__isnull=True) | Q(expiry_date__gte=now())
    ).order_by('-is_pinned', '-created_at')[:5]

    return render(
        request,
        "student/dashboard.html",
        {
            "student": student,
            "assignments": assignments,
            "notices": notices
        }
    )


def student_logout(request):
    logout(request)
    return redirect("student:student_login")

# ----------------------------
# COURSES
# ----------------------------
@student_login_required
def enroll_in_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    student = request.user.student_profile
    student.courses.add(course)
    messages.success(request, f"You have successfully enrolled in {course.name}.")
    return redirect("student:my_courses")


@student_login_required
def my_courses(request):
    student = request.user.student_profile
    query = request.GET.get('q')

    courses = student.courses.all()

    if query:
        courses = courses.filter(
            Q(name__icontains=query) |
            Q(category__icontains=query) |
            Q(description__icontains=query)
        )

    return render(
        request,
        "student/my_courses.html",
        {
            "student": student,
            "courses": courses,
            "query": query
        },
    )


@student_login_required
def course_detail(request, course_id):
    student = request.user.student_profile
    course = get_object_or_404(Course, id=course_id, id__in=student.courses.all())

    topics = course.topics.all()
    assignments = course.assignments.all()

    submissions = Submission.objects.filter(student=student, assignment__course=course)
    submission_dict = {s.assignment.id: s for s in submissions}

    form = AssignmentUploadForm()

    return render(
        request,
        "student/course_detail.html",
        {
            "course": course,
            "topics": topics,
            "assignments": assignments,
            "submission_dict": submission_dict,
            "form": form,
        },
    )


# ----------------------------
# TOPICS
# ----------------------------
@student_login_required
def course_topics(request, course_id):
    student = request.user.student_profile
    course = get_object_or_404(Course, id=course_id, id__in=student.courses.all())
    topics = course.topics.all()
    return render(
        request,
        "student/course_topics.html",
        {"course": course, "topics": topics},
    )


@student_login_required
def topic_detail(request, topic_id):
    topic = get_object_or_404(Topic, id=topic_id)

    from django.db.models import Q
    quizzes = Quiz.objects.filter(
        Q(course=topic.course) & (Q(topic=topic) | Q(topic__isnull=True))
    ).distinct()

    return render(
        request,
        "student/topic_detail.html",
        {"topic": topic, "quizzes": quizzes},
    )


# ----------------------------
# QUIZZES
# ----------------------------



@student_login_required
def take_quiz(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    questions = list(quiz.questions.all())
    total = len(questions)

    if total == 0:
        messages.warning(request, "This quiz has no questions yet.")
        return redirect("student:student_dashboard")

    index = request.session.get(f"quiz_{quiz_id}_index", 0)
    index = min(index, total - 1)
    question = questions[index]

    student = request.user

    submission, _ = QuizSubmission.objects.get_or_create(
        student=student,
        quiz=quiz,
        defaults={'score': 0}
    )

    answers = request.session.get(f"quiz_{quiz_id}_answers", {})

    if request.method == "POST":
        selected = request.POST.get("answer")

        if selected:
            answers[str(question.id)] = selected
            request.session[f"quiz_{quiz_id}_answers"] = answers

        if "next" in request.POST and index < total - 1:
            index += 1

        elif "prev" in request.POST and index > 0:
            index -= 1

        elif "submit" in request.POST:

            score = 0
            review_data = {}

            for q in questions:
                selected = answers.get(str(q.id))
                correct = q.correct_answer

                if selected == correct:
                    score += 1

                review_data[q] = {
                    "selected": selected,
                    "correct": correct,
                }

            submission.score = score
            submission.save()

            # Clear session
            request.session.pop(f"quiz_{quiz_id}_index", None)
            request.session.pop(f"quiz_{quiz_id}_answers", None)

            # Calculate percentage
            percentage = int((score / total) * 100) if total > 0 else 0

            return render(request, "student/quiz_result.html", {
                "quiz": quiz,
                "score": score,
                "total": total,
                "percentage": percentage,   # Added
                "answers": review_data,
            })

        request.session[f"quiz_{quiz_id}_index"] = index
        question = questions[index]

    saved_answer = answers.get(str(question.id), None)

    return render(request, "student/take_quiz.html", {
        "quiz": quiz,
        "question": question,
        "index": index,
        "total": total,
        "saved_answer": saved_answer,
    })


# ----------------------------
# ASSIGNMENTS
# ----------------------------

@student_login_required
def course_assignments(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    student = request.user.student_profile

    assignments = course.assignments.all()

    for assignment in assignments:
        assignment.submission = Submission.objects.filter(
            assignment=assignment,
            student=student
        ).first()

    form = AssignmentUploadForm()

    return render(
        request,
        "student/course_assignments.html",
        {
            "course": course,
            "student": student,
            "assignments": assignments,
            "form": form,
            "active_page": "assignments"
        },
    )



@student_login_required
def submit_assignment(request, assignment_id):
    assignment = get_object_or_404(Assignment, id=assignment_id)
    student = request.user.student_profile

    if request.method == "POST":
        form = AssignmentUploadForm(request.POST, request.FILES)

        if form.is_valid():
            Submission.objects.update_or_create(
                assignment=assignment,
                student=student,
                defaults={
                    "file": form.cleaned_data["file"]
                },
            )

            messages.success(request, "Assignment submitted successfully!")

            return redirect(
                "student:course_detail",
                course_id=assignment.course.id
            )

    else:
        form = AssignmentUploadForm()

    return render(
        request,
        "student/submit_assignment.html",
        {
            "assignment": assignment,
            "student": student,
            "form": form,
            "active_page": "assignments"
        },
    )


@student_login_required
def topic_assignments(request, topic_id):
    topic = get_object_or_404(Topic, id=topic_id)
    student = request.user.student_profile

    # Get assignments under this topic
    assignments = Assignment.objects.filter(topic=topic)

    # Attach submission info
    for assignment in assignments:
        assignment.submission = Submission.objects.filter(
            assignment=assignment,
            student=student
        ).first()

    form = AssignmentUploadForm()

    return render(
        request,
        "student/topic_assignments.html",
        {
            "topic": topic,
            "student": student,
            "assignments": assignments,
            "form": form,
            "active_page": "assignments"
        },
    )

@student_login_required
def all_assignments(request):
    student = request.user.student_profile

    # Get all courses of this student
    courses = student.courses.all()

    assignments_data = []

    for course in courses:
        assignments = course.assignments.all()

        for assignment in assignments:
            assignment.submission = Submission.objects.filter(
                assignment=assignment,
                student=student
            ).first()

        assignments_data.append({
            "course": course,
            "assignments": assignments
        })

    return render(
        request,
        "student/all_assignments.html",
        {
            "student": student,
            "assignments_data": assignments_data,
            "active_page": "assignments"
        }
    )


# ----------------------------
# ATTENDANCE
# ----------------------------
@student_login_required
def mark_attendance(request, topic_id):
    """ Marks student as present for a topic """
    topic = get_object_or_404(Topic, id=topic_id)
    student = request.user.student_profile

    attendance, created = Attendance.objects.get_or_create(
        topic=topic, student=student,
        defaults={"status": True}
    )

    if not created:
        if not attendance.status:  # only update if previously absent
            attendance.status = True
            attendance.save()
            messages.success(request, "Your attendance has been updated to present.")
        else:
            messages.info(request, "Your attendance is already marked as present.")
    else:
        messages.success(request, "Your attendance has been marked as present.")

    return redirect("student:topic_detail", topic_id=topic.id)

@student_login_required
def notice_board(request):
    notices = Notice.objects.filter(is_active=True).order_by('-is_pinned', '-created_at')
    return render(request, "student/notice_board.html", {"notices": notices})

@student_login_required
def id_card(request):
    student = request.user.student_profile
    return render(request, "student/id_card.html", {"student": student})