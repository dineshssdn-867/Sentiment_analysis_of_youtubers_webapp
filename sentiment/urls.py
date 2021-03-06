from django.urls import path  # Importing necessary libraries for urls
from .views import *  # Importing all the views from views.py

app_name = 'sentiment'  # Initializing app name
urlpatterns = [
    path('', HomeView.as_view(), name='home'),  # Connecting the url route to the view with namespace of home
    path('show_emotion/', FormViewEmotion.as_view(), name="show_emotion"),  # Connecting the url route to the view with namespace of show_emotion
    path('show_sentiment/', FormViewSentiment.as_view(), name="show_sentiment"), # Connecting the url route to the view with namespace of show_emotion
    path('show_emotion_result/', show_emotion, name="show_emotion_result"),  # Connecting the url route to the view with namespace of show_emotion_result
    path('show_sentiment_result/', show_sentiment, name="show_sentiment_result"), # Connecting the url route to the view with namespace of show_emotion_result
    path('show_emotion_video/', FormViewVideoEmotion.as_view(), name="show_emotion_video"),  # Connecting the url route to the view with namespace of show_emotion_video
    path('show_sentiment_video/', FormViewVideoSentiment.as_view(), name="show_sentiment_video"), # Connecting the url route to the view with namespace of show_emotion_video
    path('show_emotion_video_result/', show_emotion_video, name="show_emotion_video_result"),  # Connecting the url route to the view with namespace of show_emotion_video_result
    path('show_sentiment_video_result/', show_sentiment_video, name="show_sentiment_video_result"), # Connecting the url route to the view with namespace of show_emotion_video_result
    path('show_emotion_video_comment/', FormCommentViewVideoEmotion.as_view(), name="show_emotion_video_comment"),  # Connecting the url route to the view with namespace of show_emotion_video
    path('show_sentiment_video_comment/', FormCommentViewVideoSentiment.as_view(), name="show_sentiment_video_comment"), # Connecting the url route to the view with namespace of show_emotion_video
    path('show_emotion_video_result_commment/', show_comment_emotion_video, name="show_emotion_video_comment_result"),  # Connecting the url route to the view with namespace of show_emotion_video_result
    path('show_sentiment_video_result_commment/', show_comment_sentiment_video, name="show_sentiment_video_comment_result"), # Connecting the url route to the view with namespace of show_emotion_video_result
]
