from django.urls import path
from .views import phq9_assessment, gad7_assessment, update_followup_details

urlpatterns = [
    path('phq9/', phq9_assessment, name='phq9'),
    path('gad7/', gad7_assessment, name='gad7'),
    path('followup/<int:pk>/', update_followup_details, name='update_followup'),
]

