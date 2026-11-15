from django.contrib import admin
from django.urls import path
from login.views import login_view
from dashboard.views import dashboard_view
from exams.lvl1.views import level_one
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', login_view, name='login'),
    path('Dodawanie-i-odejmowanie-ułamków-o-jednakowych-mianownikach/', level_one, name='level-one'),
    path('logout/',auth_views.LogoutView.as_view(), name='logout'),
    path('', dashboard_view, name='dashboard'),

]
