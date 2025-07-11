from django.urls import path
from . import views

urlpatterns = [
    path("csrf/", views.csrf_view),
    path("login/", views.login_view),
    path("logout/", views.logout_view),
    path("user/", views.user_view),
    path("auth/check/", views.check_auth),
    path("change-password/", views.change_password),
]
