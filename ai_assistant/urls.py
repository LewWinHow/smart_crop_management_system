from django.urls import path

from ai_assistant.views import *

app_name = 'ai_assistant'

urlpatterns = [
    path('get_chat/', GetChat().as_view(), name='get_chat'),
    path('clear_chat/', ClearChat.as_view(), name='clear_chat'),
    path('receive_message_and_use_llm/', GetChat().as_view(), name='receive_message_and_use_llm'),
]
