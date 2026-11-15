
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings


# =====================================================
# USERS
# =====================================================

class User(AbstractUser):

    username = models.CharField(
        max_length=10,
        unique=True,
        db_column='username_login_id'
    )

    points = models.PositiveIntegerField(default=0)

    class Meta:
        db_table = 'users'

    def __str__(self):
        return self.username


# =====================================================
# LEVELS
# =====================================================

class Level(models.Model):

    level_name = models.CharField(max_length=256)

    required_points = models.PositiveIntegerField()

    class Meta:
        db_table = 'levels'

    def __str__(self):
        return self.level_name


# =====================================================
# UNLOCKED LEVELS
# =====================================================

class UnlockedLevel(models.Model):

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='unlocked_levels'
    )

    level = models.ForeignKey(
        Level,
        on_delete=models.CASCADE,
        related_name='unlocked_by_users'
    )

    class Meta:
        db_table = 'unlocked_levels'

        constraints = [
            models.UniqueConstraint(
                fields=['user', 'level'],
                name='unique_user_level'
            )
        ]

    def __str__(self):
        return f"{self.user} - {self.level}"


# =====================================================
# RESULTS
# =====================================================

class Result(models.Model):

    class Status(models.TextChoices):
        IN_PROGRESS = 'in_progress', 'W trakcie'
        COMPLETED = 'completed', 'Zakończony'
        ABANDONED = 'abandoned', 'Porzucony'

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='results'
    )

    level = models.ForeignKey(
        Level,
        on_delete=models.CASCADE,
        related_name='results'
    )

    started_at = models.DateTimeField(auto_now_add=True)

    finished_at = models.DateTimeField(
        null=True,
        blank=True
    )

    result = models.PositiveIntegerField(default=0)

    max_result = models.PositiveIntegerField(default=0)

    tips_ai = models.PositiveIntegerField(default=0)

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.IN_PROGRESS
    )

    class Meta:
        db_table = 'results'
        ordering = ['-started_at']

    def __str__(self):
        return f"{self.user} - {self.level}: {self.result}"


# =====================================================
# QUESTIONS
# =====================================================

class Question(models.Model):

    class QuestionType(models.TextChoices):
        SINGLE_CHOICE = 'single_choice', 'Jedna odpowiedź'
        MULTIPLE_CHOICE = 'multiple_choice', 'Wiele odpowiedzi'
        TRUE_FALSE = 'true_false', 'Prawda / Fałsz'
        OPEN = 'open', 'Otwarta odpowiedź'
        FILL_BLANK = 'fill_blank', 'Uzupełnianie'

    level = models.ForeignKey(
        Level,
        on_delete=models.CASCADE,
        related_name='questions'
    )

    question = models.TextField()

    question_type = models.CharField(
        max_length=30,
        choices=QuestionType.choices,
        default=QuestionType.SINGLE_CHOICE
    )

    difficulty = models.PositiveSmallIntegerField(default=1)

    points = models.PositiveIntegerField(default=1)

    explanation = models.TextField(
        blank=True,
        default=''
    )

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'questions'
        indexes = [
            models.Index(
                fields=['level', 'is_active'],
                name='question_level_active_idx'
            )
        ]

    def __str__(self):
        return self.question[:50]


# =====================================================
# ANSWERS
# =====================================================

class Answer(models.Model):

    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name='answers'
    )

    answer_text = models.TextField()

    is_correct = models.BooleanField(default=False)

    error_type = models.CharField(
        max_length=50,
        null=True,
        blank=True
    )

    explanation = models.TextField(
        blank=True,
        default=''
    )

    class Meta:
        db_table = 'answers'
        indexes = [
            models.Index(
                fields=['question'],
                name='answer_question_idx'
            )
        ]

    def __str__(self):
        return self.answer_text[:50]


# =====================================================
# STUDENT ANSWERS
# =====================================================

class StudentAnswer(models.Model):

    result = models.ForeignKey(
        Result,
        on_delete=models.CASCADE,
        related_name='student_answers'
    )

    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name='student_answers'
    )

    answer = models.ForeignKey(
        Answer,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='student_answers'
    )

    is_correct = models.BooleanField(
        null=True,
        blank=True
    )

    answered_at = models.DateTimeField(
        null=True,
        blank=True
    )

    class Meta:
        db_table = 'student_answers'

        constraints = [
            models.UniqueConstraint(
                fields=['result', 'question'],
                name='unique_result_question'
            )
        ]

    def __str__(self):
        return f"{self.result} - {self.question}"
