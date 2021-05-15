from django.urls import path  # Importing necessary libraries for urls
from .views import *  # Importing all the views from views.py


app_name = "users" # Initializing app name
urlpatterns = [
    path('register/', RegisterView.as_view(), name="register"),  # Connecting the url route to the view with namespace of register
    path('login/', UserLoginView.as_view(), name="login"),  # Connecting the url route to the view with namespace of login
    path('logout/', UserLogoutView.as_view(), name="logout"),  # Connecting the url route to the view with namespace of logout
]
