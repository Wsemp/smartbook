from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import (
    User,
    Level,
    UnlockedLevel,
    Result,
    Question,
    Answer,
    StudentAnswer
)


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('id', 'username', 'points', 'is_staff')
    search_fields = ('username',)
    list_filter = ('is_staff', 'is_active')


@admin.register(Level)
class LevelAdmin(admin.ModelAdmin):
    list_display = ('id', 'level_name', 'required_points', 'url_path')
    search_fields = ('level_name',)
    ordering = ('id',)


@admin.register(UnlockedLevel)
class UnlockedLevelAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'level')
    list_filter = ('level',)
    search_fields = ('user__username', 'level__level_name')


@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'user',
        'level',
        'started_at',
        'finished_at',
        'status',
        'result',
        'max_result',
        'tips_ai',
    )

    list_filter = (
        'level',
        'status',
        'started_at',
    )

    search_fields = (
        'user__username',
        'level__level_name',
    )

    ordering = ('-started_at',)

    readonly_fields = ('started_at',)


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'level',
        'question_short',
        'question_type',
        'difficulty',
        'points',
        'is_active',
        'created_at',
    )

    list_filter = (
        'level',
        'question_type',
        'difficulty',
        'is_active',
    )

    search_fields = ('question', 'explanation')

    ordering = ('level', 'difficulty')

    readonly_fields = ('created_at', 'updated_at')

    @admin.display(description='Treść pytania')
    def question_short(self, obj):
        return obj.question[:70]


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'question',
        'answer_short',
        'is_correct',
        'error_type',
    )

    list_filter = (
        'is_correct',
        'error_type',
        'question__level',
    )

    search_fields = (
        'answer_text',
        'question__question',
        'explanation',
    )

    @admin.display(description='Treść odpowiedzi')
    def answer_short(self, obj):
        return obj.answer_text[:70]


@admin.register(StudentAnswer)
class StudentAnswerAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'result',
        'question',
        'answer',
        'is_correct',
        'answered_at',
    )

    list_filter = (
        'is_correct',
        'result__level',
        'answered_at',
    )

    search_fields = (
        'result__user__username',
        'question__question',
        'answer__answer_text',
    )

    readonly_fields = ('answered_at',)

    ordering = ('-answered_at',)
