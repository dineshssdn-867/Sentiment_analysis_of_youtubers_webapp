from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.http import HttpResponse


# Create your views here.
class HomeView(TemplateView):
    template_name ='sentiment/index.html'

class FormView(TemplateView):
    template_name ='sentiment/sentiment_form.html'

def show(request):
    channel_id=request.POST.get('channel_id')
    publish_date_after=request.POST.get('publish_date_after')
    publish_date_before=request.POST.get('publish_date_before')
    print(publish_date_after)
    print(publish_date_before)
    return HttpResponse("Http request is: "+request.method)  
    
    

