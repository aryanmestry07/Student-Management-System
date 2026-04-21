from django.db import models
from django.contrib.auth.models import User

# -------------------
# COURSE, TOPIC, ASSIGNMENT
# -------------------

class Course(models.Model):
    name = models.CharField(max_length=255)
    category = models.CharField(max_length=100)
    description = models.TextField()
    duration = models.IntegerField(help_text="Duration in months") # Changed to months for Bandra Campus logic
    price = models.DecimalField(max_digits=10, decimal_places=2)
    total_topics = models.IntegerField(default=0)

    class Meta:
        verbose_name_plural = "Courses"

    def __str__(self):
        return self.name


class Topic(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="topics")
    title = models.CharField(max_length=200)
    description = models.TextField()
    notes_file = models.FileField(upload_to='notes/', null=True, blank=True)

    def __str__(self):
        return f"{self.title} | {self.course.name}"


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

    class Meta:
        verbose_name_plural = "Quizzes"

    def __str__(self):
        scope = self.topic.title if self.topic else "General Catalog"
        return f"{self.title} | {scope}"


class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name="questions")
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, null=True, blank=True)
    text = models.TextField()
    
    # Updated to default to empty string to prevent "None" appearing in UI
    option_a = models.CharField(max_length=255, default="")
    option_b = models.CharField(max_length=255, default="")
    option_c = models.CharField(max_length=255, default="")
    option_d = models.CharField(max_length=255, default="")
    
    CORRECT_CHOICES = [("A", "Option A"), ("B", "Option B"), ("C", "Option C"), ("D", "Option D")]
    correct_answer = models.CharField(max_length=1, choices=CORRECT_CHOICES)

    def __str__(self):
        return f"Q: {self.text[:50]}..."

    @property
    def get_options(self):
        """
        Returns a clean dictionary of options. 
        Ensures even empty options return a string to avoid 'None' in templates.
        """
        return {
            "A": self.option_a or "",
            "B": self.option_b or "",
            "C": self.option_c or "",
            "D": self.option_d or "",
        }


# -------------------
# SUBMISSION & STUDENT ANSWERS
# -------------------

class QuizSubmission(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name="quiz_submissions")
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name="submissions")
    score = models.FloatField(default=0)
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.username} -> {self.quiz.title} ({self.score})"


class StudentAnswer(models.Model):
    submission = models.ForeignKey(QuizSubmission, on_delete=models.CASCADE, related_name="answers")
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    selected_answer = models.CharField(max_length=1, choices=Question.CORRECT_CHOICES)
    is_correct = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        # Auto-validate the answer before saving
        self.is_correct = (self.selected_answer == self.question.correct_answer)
        super().save(*args, **kwargs)

    def get_selected_text(self):
        # Dynamically fetch the text based on the letter
        return getattr(self.question, f"option_{self.selected_answer.lower()}", "")


# -------------------
# INSTITUTIONAL BROADCASTS
# -------------------

class Notice(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_pinned = models.BooleanField(default=False)
    expiry_date = models.DateField(null=True, blank=True)
    posted_by = models.CharField(max_length=100, default="ICE_ADMIN") # Brand consistency

    def __str__(self):
        return f"{'[PIN] ' if self.is_pinned else ''}{self.title}"