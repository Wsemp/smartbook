from database.models import Question

def get_questions_by_level(level_id):
    questions = Question.objects.filter(
        level_id=level_id,
        is_active=True
    ).prefetch_related("answer_set")

    return questions