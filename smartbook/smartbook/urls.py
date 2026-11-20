from django.contrib import admin
from django.urls import path
from login.views import login_view
from dashboard.views import dashboard_view
from exams.lvl1.views import level_view
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', login_view, name='login'),
    path('logout/',auth_views.LogoutView.as_view(), name='logout'),
    path('', dashboard_view, name='dashboard'),
    path('<slug:url_path>/', level_view, name='level-detail'),
    # path('dodawanie-i-odejmowanie-ulamkow-o-roznych-mianownikach/', level_one, name='level-one'),
    # path('mnozenie-ulamka-przez-liczbe-naturalna/', level_one, name='level-one'),
    # path('obliczanie-ulamka-danej-liczby/', level_one, name='level-one'),
    # path('mnozenie-ulamkow-zwyklych/', level_one, name='level-one'),
    # path('dzielenie-ulamkow-przez-liczby-naturalne/', level_one, name='level-one'),
    # path('dzielenie-ulamkow-zwyklych/', level_one, name='level-one'),
    # path('wyznaczanie-liczby-ktorej-czesc-jest-podana/', level_one, name='level-one'),
]
