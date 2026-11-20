
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Prefetch

from database.models import Question, Answer, Level


def level_view(request, url_path):

    # Pobieramy poziom na podstawie ścieżki URL
    level = get_object_or_404(Level, url_path=url_path)

    level_id = level.id
    session_key = f"questions_level_{level_id}"

    # Losujemy pytania tylko przy pierwszym wejściu na test
    if session_key not in request.session:
        question_ids = list(
            Question.objects.filter(
                level_id=level_id,
                is_active=True
            ).order_by("?").values_list("id", flat=True)
        )

        request.session[session_key] = question_ids

    question_ids = request.session[session_key]

    # Jedno pytanie na stronę
    paginator = Paginator(question_ids, 1)
    page_obj = paginator.get_page(request.GET.get("page", 1))

    if not page_obj.object_list:
        return render(request, "lvl1/lvl1.html", {
            "question": None,
            "page_obj": page_obj,
            "level": level,
        })

    question_id = page_obj.object_list[0]

    # Pobieramy konkretne pytanie i losujemy odpowiedzi
    question = get_object_or_404(
        Question.objects.prefetch_related(
            Prefetch(
                "answers",
                queryset=Answer.objects.order_by("?")
            )
        ),
        id=question_id,
        level_id=level_id,
        is_active=True
    )

    context = {
        "question": question,
        "page_obj": page_obj,
        "level": level,
    }

    return render(request, "lvl1/lvl1.html", context)
