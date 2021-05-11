import json
import re
from collections import OrderedDict
from operator import itemgetter
import ktrain
import nltk
import requests
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.generic.base import TemplateView
from youtube_transcript_api import YouTubeTranscriptApi

predictor_1 = ktrain.load_predictor(r'C:\Users\Dinesh\Desktop\Sentiment\models\my_new_predictor_emotion')
predictor_2 = ktrain.load_predictor(r'C:\Users\Dinesh\Desktop\Sentiment\models\my_new_predictor_intent')


# Create your views here.
class HomeView(TemplateView):
    template_name = 'sentiment/index.html'


class FormViewEmotion(TemplateView):
    template_name = 'sentiment/sentiment_form.html'


class FormViewIntent(TemplateView):
    template_name = 'sentiment/sentiment_intent_form.html'


@login_required(login_url='/users/login')
def show_emotion(request):
    channel_id = request.POST.get('channel_id')
    publish_date_after = request.POST.get('publish_date_after')
    publish_date_before = request.POST.get('publish_date_before')
    video_id = get_youtube_data(channel_id, publish_date_after, publish_date_before)
    if len(video_id) == 0:
        messages.error(request, 'Services are not working properly or invalid data')
        return HttpResponseRedirect(reverse('sentiment:show_emotion'))
    texts = get_subtitles(video_id)
    if texts == '':
        messages.error(request, 'Please check the subtitles setting of your channel')
        return HttpResponseRedirect(reverse('sentiment:show_emotion'))
    texts = get_clean_data(texts)
    predicitions = predict_emotion(texts)
    emotion_labels = []
    emotion_probabilties = []
    for predicition in predicitions:
        emotion_labels.append(predicition[0])
        emotion_probabilties.append(predicition[1])
    context = {
        'labels': emotion_labels,
        'probabilites': emotion_probabilties
    }
    return render(request, 'sentiment/results.html', context=context)


def get_youtube_data(channel_id, publish_date_after, publish_date_before):
    publish_date_after = publish_date_after + 'T00:00:00Z'  # hardcoded publish before date
    publish_date_before = publish_date_before + 'T00:00:00Z'  # hardcoded publish before date
    video_id = []
    x = requests.get(
        'https://www.googleapis.com/youtube/v3/search?key=AIzaSyDnIqoMPASXgKPkzxlcy4krIPOHtJOJ998&channelId=' + channel_id + '&part=snippet,id&order=date&publishedBefore=+' + publish_date_before + '&publishedAfter=' + publish_date_after)  # getting the data of channel
    print(x.status_code)
    if x.status_code == 200:
        values = json.loads(x.text)# converting the string data to json
        print(values)
        num = len(values['items'])  # getting the number of videos
        for i in range(0, num):
            video_id.append(values['items'][i]['id']['videoId'])  # appending the ids to list
        return video_id
    else:
        return video_id


def get_subtitles(video_id):
    texts = ''  # adding the subtitles
    try:
        for id in video_id:
            transcript_list = YouTubeTranscriptApi.list_transcripts(id)  # fetching the transcript list
            # iterate over all available transcripts
            for transcript in transcript_list:
                contents = transcript.translate('en').fetch()  # translate the transcript into english
                for content in contents:
                    texts = texts + content['text']
                    texts = texts + " "
        return texts
    except:
        print("Please check the channel or video options regarding subtitles")
        texts = ''
        return texts


def get_clean_data(texts):
    texts = texts.lower()
    texts = texts.replace(r"(http|@)\S+", "")
    texts = texts.replace(r"::", ": :")
    texts = texts.replace(r"’", "'")
    texts = texts.replace(r"[^a-z\':_]", " ")
    pattern = re.compile(r"(.)\1{2,}", re.DOTALL)
    pattern = str(pattern)
    texts = texts.replace(pattern, r"\1")
    texts = texts.replace(r"(can't|cannot)", 'can not')
    texts = texts.replace(r"n't", ' not')
    stopwords = nltk.corpus.stopwords.words('english')
    stopwords.remove('not')
    stopwords.remove('nor')
    stopwords.remove('no')
    texts = ' '.join([word for word in texts.split() if word not in stopwords])
    return texts


def predict_emotion(texts):
    return predictor_1.predict(texts)


def predict_intent(texts):
    return predictor_2.predict(texts)


@login_required(login_url='/users/login')
def show_intent(request):
    channel_id = request.POST.get('channel_id')
    publish_date_after = request.POST.get('publish_date_after')
    publish_date_before = request.POST.get('publish_date_before')
    video_id = get_youtube_data(channel_id, publish_date_after, publish_date_before)
    if len(video_id) == 0:
        messages.error(request, 'Services are not working properly or invalid data')
        return HttpResponseRedirect(reverse('sentiment:show_intent'))
    texts = get_subtitles(video_id)
    if texts == '':
        messages.error(request, 'Please check the subtitles setting of your channel')
        return HttpResponseRedirect(reverse('sentiment:show_intent'))
    predicitions = predictor_2.predict("Hello",return_proba=True)  # tesing it for youtube subitiles obtained from API services
    labels = predictor_2.get_classes()
    x = []
    y = []
    intent = {}

    i = 0

    for predicition in predicitions:  # appending different probabilities of predicitions in x and y
        intent[labels[i]] = predicition
        i = i + 1

    intent = OrderedDict(sorted(intent.items(), key=itemgetter(1)))

    i = 0
    # getting the last 5 values
    for key in intent.keys():
        if i >= 148:
            x.append(key)
            y.append(intent[key])
        i = i + 1

    context = {
        'labels': x,
        'probabilites': y
    }
    return render(request, 'sentiment/results_intent.html', context=context)
