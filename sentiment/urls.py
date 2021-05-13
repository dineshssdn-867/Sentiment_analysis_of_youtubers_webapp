from django.urls import path
from .views import *

app_name = 'sentiment'
urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('show_emotion/', FormViewEmotion.as_view(), name="show_emotion"),
    path('show_intent/', FormViewIntent.as_view(), name="show_intent"),
    path('show_emotion_result/', show_emotion, name="show_emotion_result"),
    path('show_emotion_video/', FormViewVideoEmotion.as_view(), name="show_emotion_video"),
    path('show_intent_video/', FormViewVideoIntent.as_view(), name="show_intent_video"),
    path('show_emotion_video_result/', show_emotion_video, name="show_emotion_video_result"),
    path('show_intent_video_result/', show_intent_video, name="show_intent_video_result"),
]
