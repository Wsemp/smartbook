from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from ..utils import get_questions_by_level

@login_required
def level_one(request):

    questions = get_questions_by_level(1)

    context = {'questions': questions}

    return render(request, 'lvl1/lvl1.html', context)
