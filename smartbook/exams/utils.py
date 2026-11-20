from database.models import Question, Answer
from django.db.models import Prefetch

def get_questions_by_level(level_id):
    questions = Question.objects.filter(
        level_id=level_id,
        is_active=True
    ).prefetch_related(
        Prefetch(
            "answers",
            queryset=Answer.objects.order_by("?")
        )
    ).order_by("?")

    return questions