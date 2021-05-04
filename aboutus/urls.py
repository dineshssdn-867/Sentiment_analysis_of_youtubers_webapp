from django.urls import path
from .views import *

app_name = "aboutus"
urlpatterns = [
    path('', AboutUsView.as_view(), name="about"),

]
