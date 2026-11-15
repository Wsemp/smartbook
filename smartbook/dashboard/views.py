from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from database.models import Level

@login_required
def dashboard_view(request):

    levels = Level.objects.all()

    context = {
        'levels': levels
    }

    return render(request, 'dashboard/dashboard.html', context)
