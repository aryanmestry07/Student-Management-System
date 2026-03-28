#myapp/models.py
from django.db import models
from django.contrib.auth.models import User  # Or link to your Student model


# -------------------
# COURSE, TOPIC, ASSIGNMENT
# -------------------

class Course(models.Model):
    name = models.CharField(max_length=255)
    category = models.CharField(max_length=100)
    description = models.TextField()
    duration = models.IntegerField(help_text="Duration in hours")
    price = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return self.name


class Topic(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="topics")
    title = models.CharField(max_length=200)
    description = models.TextField()

    def __str__(self):
        return f"{self.title} ({self.course.name})"


class Assignment(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="assignments")
    title = models.CharField(max_length=200)
    description = models.TextField()
    due_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.title} ({self.course.name})"


# -------------------
# QUIZ & QUESTION
# -------------------

class Quiz(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="quizzes")
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name="quizzes", null=True, blank=True)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        topic_name = self.topic.title if self.topic else "General"
        return f"{self.title} ({self.course.name} - {topic_name})"


# models.py
class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name="questions")
    topic = models.ForeignKey("Topic", on_delete=models.CASCADE, null=True, blank=True)
    text = models.TextField()
    option_a = models.CharField(max_length=255, blank=True, null=True)
    option_b = models.CharField(max_length=255, blank=True, null=True)
    option_c = models.CharField(max_length=255, blank=True, null=True)
    option_d = models.CharField(max_length=255, blank=True, null=True)
    correct_answer = models.CharField(max_length=1, choices=[("A", "A"), ("B", "B"), ("C", "C"), ("D", "D")])

    def get_correct_answer_text(self):
        mapping = {
            "A": self.option_a,
            "B": self.option_b,
            "C": self.option_c,
            "D": self.option_d,
        }
        return mapping.get(self.correct_answer, "")

    @property
    def get_options(self):
        return {
            "A": self.option_a,
            "B": self.option_b,
            "C": self.option_c,
            "D": self.option_d,
        }


# -------------------
# SUBMISSION & STUDENT ANSWERS
# -------------------

class QuizSubmission(models.Model):  # ✅ renamed to avoid clash
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name="quiz_submissions")
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name="submissions")
    score = models.FloatField(default=0)
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.username} - {self.quiz.title}"


class StudentAnswer(models.Model):
    submission = models.ForeignKey("QuizSubmission", on_delete=models.CASCADE, related_name="answers")
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    selected_answer = models.CharField(
        max_length=1,
        choices=[('A', 'Option A'), ('B', 'Option B'), ('C', 'Option C'), ('D', 'Option D')]
    )
    is_correct = models.BooleanField(default=False, editable=False)

    def save(self, *args, **kwargs):
        self.is_correct = (self.selected_answer == self.question.correct_answer)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.submission.student.username} - {self.question.text[:30]}... -> {self.selected_answer}"

    # ✅ Get actual text of student’s chosen option
    def get_selected_answer_text(self):
        return getattr(self.question, f"option_{self.selected_answer.lower()}", None)
    
class Notice(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_pinned = models.BooleanField(default=False)
    expiry_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.title