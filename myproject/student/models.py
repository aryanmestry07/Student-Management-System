# student/models.py

from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now
# pyrefly: ignore [missing-import]
from myapp.models import Course, Topic, Assignment


class Student(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="student_profile"
    )

    middle_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50)

    phone = models.CharField(max_length=15)
    birthdate = models.DateField(blank=True, null=True)
    education = models.CharField(max_length=255, blank=True, null=True)

    enrollment_date = models.DateField(auto_now_add=True)

    courses = models.ManyToManyField(
        Course,
        related_name="enrolled_students",
        blank=True
    )

    # ================= NEW FINANCIAL SYSTEM =================
    total_fees = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    paid_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    # ================= AUTO CALCULATED =================
    @property
    def pending_fees(self):
        return self.total_fees - self.paid_amount

    @property
    def fees_status(self):
        if self.paid_amount == 0:
            return "Pending"
        elif self.paid_amount >= self.total_fees:
            return "Paid"
        else:
            return "Partially Paid"

    # ================= ROLL NUMBER =================
    roll_number = models.CharField(max_length=20, unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.roll_number:
            year = now().year

            last_student = Student.objects.filter(
                roll_number__startswith=f"RN{year}"
            ).order_by('roll_number').last()

            if last_student and last_student.roll_number:
                try:
                    last_count = int(last_student.roll_number[6:])
                except ValueError:
                    last_count = 0
            else:
                last_count = 0

            self.roll_number = f"RN{year}{last_count + 1:03d}"

        super().save(*args, **kwargs)

    # ================= NAME =================
    @property
    def full_name(self):
        return f"{self.user.first_name} {self.middle_name or ''} {self.last_name}".strip()

    def __str__(self):
        return f"{self.full_name} ({self.roll_number})"

    class Meta:
        ordering = ['-enrollment_date']

class Submission(models.Model):
    """Submissions made by students for assignments"""
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE, related_name="submissions")
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="submissions")
    file = models.FileField(upload_to="submissions/")
    submitted_at = models.DateTimeField(auto_now_add=True)
    graded = models.BooleanField(default=False)
    grade = models.CharField(max_length=10, blank=True, null=True)
    feedback = models.TextField(blank=True, null=True)

    class Meta:
        unique_together = ('assignment', 'student')

    def __str__(self):
        return f"{self.student.user.username} → {self.assignment.title}"

class Attendance(models.Model):
    LECTURE_TYPE_CHOICES = [
        ('theory', 'Theory'),
        ('practical', 'Practical'),
    ]

    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name="attendance")
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="attendance")

    date = models.DateField(auto_now_add=True)
    marked_at = models.DateTimeField(auto_now_add=True)  # ✅ time stored

    status = models.BooleanField(default=True)

    # ✅ Lecture type (ONLY ONCE)
    lecture_type = models.CharField(
        max_length=10,
        choices=LECTURE_TYPE_CHOICES,
        default='theory'
    )

    class Meta:
        unique_together = ('topic', 'student', 'date')

    def __str__(self):
        return f"{self.student.user.username} - {self.topic.title} - {self.date} - {'Present' if self.status else 'Absent'}"
    

class QuizAttempt(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)

    is_completed = models.BooleanField(default=False)
    score = models.IntegerField(default=0)
    attempted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('student', 'topic')

    def __str__(self):
        return f"{self.student} - {self.topic} - Completed: {self.is_completed}"
    

class FinalExam(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    total_marks = models.IntegerField(default=0)
    obtained_marks = models.IntegerField(blank=True, null=True)

    is_completed = models.BooleanField(default=False)
    attempted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student} - {self.course} Exam"
    


class Result(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    marks = models.IntegerField()
    status = models.CharField(max_length=10, choices=[
        ('pass', 'Pass'),
        ('fail', 'Fail')
    ])

    created_at = models.DateTimeField(auto_now_add=True)
    total_marks = models.IntegerField(default=0)
    percentage = models.FloatField(default=0)

    def __str__(self):
        return f"{self.student} - {self.course} - {self.status}"
    
    
import uuid



class Certificate(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    # ✅ Upload / Generated File
    certificate_file = models.FileField(upload_to='certificates/', blank=True, null=True)

    # ✅ Status
    generated = models.BooleanField(default=False)
    generated_at = models.DateTimeField(blank=True, null=True)

    # ✅ Extra Info (for manual/admin use)
    marks = models.IntegerField(blank=True, null=True)
    year = models.IntegerField(blank=True, null=True)

    # ✅ Unique Certificate ID
    certificate_id = models.CharField(max_length=20, unique=True, blank=True)

    def save(self, *args, **kwargs):
        # 🔹 Auto Certificate ID
        if not self.certificate_id:
            self.certificate_id = f"CERT-{uuid.uuid4().hex[:8].upper()}"

        # 🔹 Auto set generated fields when file uploaded
        if self.certificate_file and not self.generated:
            self.generated = True
            self.generated_at = now()

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.student.full_name} - {self.course.name} - {self.certificate_id}"