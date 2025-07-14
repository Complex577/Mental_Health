from django.urls import path
from . import views

urlpatterns = [
    path("csrf/", views.csrf_view),
    path("login/", views.login_view),
    path("logout/", views.logout_view),
    path("user/", views.user_view),
    path("auth/check/", views.check_auth),
    path("change-password/", views.change_password),
    path("dashboard/", views.dashboard_view),
    path("phq9-stats/", views.phq9_stats),
    path("gad7-stats/", views.gad7_stats),
    path("sdq-stats/", views.sdq_stats),
    path("referrals/", views.referral_stats_view),

    path('content-nodes/', views.list_root_nodes, name='contentnode-list'),
    path('create/content-nodes/', views.create_node, name='contentnode-create'),
    path('update/content-nodes/<int:pk>/', views.update_node, name='contentnode-update'),
    path('delete/content-nodes/<int:pk>/', views.delete_node, name='contentnode-delete'),
]
