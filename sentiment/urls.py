from django.urls import path
from .views import *

app_name='sentiment'
urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('show_emotion/', FormViewEmotion.as_view(), name="show_emotion"),
    path('show_intent/', FormViewIntent.as_view(), name="show_intent"),
    path('show_emotion_result/', show_emotion, name="show_emotion_result"),
    path('show_intent_result/', show_intent, name="show_intent_result"),
]
