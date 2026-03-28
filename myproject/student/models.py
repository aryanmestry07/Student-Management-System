#student/models.py
from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now
from myapp.models import Course, Topic, Assignment


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="student_profile")
    middle_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=15)
    birthdate = models.DateField(blank=True, null=True)
    education = models.CharField(max_length=255, blank=True, null=True)
    enrollment_date = models.DateField(auto_now_add=True)
    courses = models.ManyToManyField(Course, related_name="enrolled_students")
    id_card_generated = models.BooleanField(default=False)

    roll_number = models.CharField(max_length=20, blank=True)

    def save(self, *args, **kwargs):
        if not self.roll_number:
            year = now().year

            last_student = Student.objects.filter(
                roll_number__startswith=f"RN{year}"
            ).order_by('-roll_number').first()

            if last_student:
                last_number = int(last_student.roll_number[-3:])
                new_number = last_number + 1
            else:
                new_number = 1

            self.roll_number = f"RN{year}{new_number:03d}"

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.first_name} {self.middle_name or ''} {self.last_name} ({self.roll_number})".strip()

class Submission(models.Model):
    """Submissions made by students for assignments"""
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE, related_name="submissions")
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="submissions")
    file = models.FileField(upload_to="submissions/")
    submitted_at = models.DateTimeField(auto_now_add=True)
    graded = models.BooleanField(default=False)
    grade = models.CharField(max_length=10, blank=True, null=True)
    feedback = models.TextField(blank=True, null=True)  # Teacher feedback

    class Meta:
        unique_together = ('assignment', 'student')  # Each student submits once

    def __str__(self):
        return f"{self.student.user.username} → {self.assignment.title}"


class Attendance(models.Model):
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name="attendance")
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="attendance")
    date = models.DateField(auto_now_add=True)
    status = models.BooleanField(default=False)

    class Meta:
        unique_together = ('topic', 'student')

    def __str__(self):
        return f"{self.student.user.username} - {self.topic.title} - {'Present' if self.status else 'Absent'}"


