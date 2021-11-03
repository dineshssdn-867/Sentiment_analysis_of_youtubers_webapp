from django.urls import path  # Importing necessary libraries for urls
from .views import *  # Importing all the views from views.py

app_name = "aboutus"  # Initializing app name
urlpatterns = [
    path('', AboutUsView.as_view(), name="about"),  # Connecting the url route to the view with namespace of about

]
