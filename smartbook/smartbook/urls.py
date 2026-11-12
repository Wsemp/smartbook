from django.contrib import admin
from django.urls import path
from login.views import login_view
from dashboard.views import dashboard_view
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', login_view, name='login'),
    path('logout/',auth_views.LogoutView.as_view(), name='logout'),
    path('', dashboard_view, name='dashboard'),
]
