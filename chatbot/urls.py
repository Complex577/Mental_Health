# chatbot/urls.py
from django.urls import path
from .views import akili_chat
from .views import akili_chat_deepseek

urlpatterns = [
    path("ask/", akili_chat, name="akili_chat"),
    path("ask_akili/", akili_chat_deepseek, name="akili_chat_deepseek")
]
