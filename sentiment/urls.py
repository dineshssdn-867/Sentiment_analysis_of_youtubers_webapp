from django.urls import path
from .views import HomeView

app_name='sentiment'
urlpatterns = [
    path('', HomeView.as_view(), name='home')
]
