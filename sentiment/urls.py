from django.urls import path
from .views import *

app_name='sentiment'
urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('sentimentform/', FormView.as_view(), name='form'),
    path('show/', show, name="show")
]
