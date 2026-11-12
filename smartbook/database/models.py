
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings


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


class Level(models.Model):

    level_name = models.CharField(max_length=256)

    required_points = models.PositiveIntegerField()

    class Meta:
        db_table = 'levels'

    def __str__(self):
        return self.level_name


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


class Result(models.Model):

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

    date = models.DateField(auto_now_add=True)

    result = models.PositiveIntegerField()

    max_result = models.PositiveIntegerField()

    tips_ai = models.PositiveIntegerField(default=0)

    start_time = models.TimeField()

    end_time = models.TimeField()

    class Meta:
        db_table = 'results'
        ordering = ['-date']

    def __str__(self):
        return f"{self.user} - {self.level}: {self.result}"


class Question(models.Model):

    level = models.ForeignKey(
        Level,
        on_delete=models.CASCADE,
        related_name='questions'
    )

    question = models.TextField()

    class Meta:
        db_table = 'questions'

    def __str__(self):
        return self.question[:50]
