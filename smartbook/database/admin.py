from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import (
    User,
    Level,
    UnlockedLevel,
    Result,
    Question
)


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('id', 'username', 'points', 'is_staff')
    search_fields = ('username',)
    list_filter = ('is_staff', 'is_active')


@admin.register(Level)
class LevelAdmin(admin.ModelAdmin):
    list_display = ('id', 'level_name', 'required_points')
    search_fields = ('level_name',)


@admin.register(UnlockedLevel)
class UnlockedLevelAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'level')
    list_filter = ('level',)
    search_fields = ('user__username',)


@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'level',
        'date',
        'result',
        'max_result'
    )
    list_filter = ('level', 'date')
    search_fields = ('user__username',)


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('id', 'level', 'question')
    list_filter = ('level',)
    search_fields = ('question',)
