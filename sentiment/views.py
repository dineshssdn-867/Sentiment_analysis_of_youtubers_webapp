import json  # Importing json library for parsing api output
import re  # Importing re module for cleaning data
from collections import OrderedDict  # Importing ordered dict for sorting the dictionary data
from operator import itemgetter  # Importing item getter for getting the value for key in the dictionary data
from typing import Any, AnyStr  # Using to define the type

import ktrain  # Importing ktrain for getting the predictor of deep learning model
import nltk  # Importing nltk module for cleaning data and removing stopwords
import requests  # Importing requests module for requesting the data from api
from django.contrib import messages  # Importing messages module for showing errors
from django.contrib.auth.decorators import login_required  # Importing decorator for verifying the authenticated user
from django.http import HttpResponseRedirect  # If any error caused it will help to redirect
from django.shortcuts import render  # Jinja template engine will parse the contents using render
from django.urls import reverse  # Used in redirecting
from django.views.generic.base import TemplateView  # Importing template class based views
from youtube_transcript_api import \
    YouTubeTranscriptApi  # This library will help to fetch to subtitles of youtubers using the video ids
from django.views.decorators.cache import cache_page  # this library is used for caching


predictor_emotion = ktrain.load_predictor('models/my_new_predictor_emotion')  # Initialize the emotion predictor using ktrain as a global variable to improve performance
predictor_intent = ktrain.load_predictor('models/my_new_predictor_intent')  # Initialize the intent predictor using ktrain as a global variable to improve performance

predictor_emotion.batch_size = 128
predictor_intent.batch_size = 128


class HomeView(TemplateView):  # Initializing template for template view
    template_name = 'sentiment/index.html'


class FormViewEmotion(TemplateView):  # Initializing template for template view
    template_name = 'sentiment/sentiment_emotion_form.html'


class FormViewIntent(TemplateView):  # Initializing template for template view
    template_name = 'sentiment/sentiment_intent_form.html'


class FormViewVideoEmotion(TemplateView):  # Initializing template for template view
    template_name = 'sentiment/sentiment_form_emotion_video.html'


class FormViewVideoIntent(TemplateView):  # Initializing template for template view
    template_name = 'sentiment/sentiment_intent_form_video.html'


@login_required(login_url='/users/login')  # Checking if the user is authenticated
def show_emotion(request: AnyStr) -> Any:
    channel_id = request.POST.get('channel_id')  # Getting the channel/video id from the form using post method
    publish_date_after = request.POST.get(
        'publish_date_after')  # Getting the publish_date_after from the form using post method
    publish_date_before = request.POST.get(
        'publish_date_before')  # Getting the publish_date_before from the form using post method
    video_ids = get_youtube_data(channel_id, publish_date_after,
                                 publish_date_before)  # Getting the video ids using get_youtube_data method

    if len(video_ids) == 0:  # Some basic validations
        messages.error(request,
                       'Services are not working properly or invalid data')  # adding the errors in messages list which will be shown in message.html template
        return HttpResponseRedirect(
            reverse('sentiment:show_emotion'))  # Redirecting to form page if there are any errors.

    texts, error_ = get_subtitles(video_ids)  # Getting the subtitles using get_subtitles method
    if texts == '':  # Some basic validations
        messages.error(request,
                       'Please check the subtitles setting of your channel/video')  # adding the errors in messages list which will be shown in message.html template
        return HttpResponseRedirect(
            reverse('sentiment:show_emotion'))  # Redirecting to form page if there are any errors
    if len(error_) > 0:  # Some basic validations
        messages.error(request,
                       error_)  # adding the errors in messages list which will be shown in message.html template

    texts = get_clean_data(texts)  # Getting the cleaned text using get_clean_data method

    emotion_predictions = predictor_emotion.predict(texts, return_proba=True)  # predicting on the cleaned text
    emotion_labels = predictor_emotion.get_classes()  # getting the labels

    context = {  # setting the context with our data
        'labels': emotion_labels,
        'probabilities': emotion_predictions,
    }
    return render(request, 'sentiment/results_emotion.html',
                  context=context)  # rendering template with out data using jinja template engine


def get_youtube_data(channel_id: AnyStr, publish_date_after: AnyStr, publish_date_before: AnyStr) -> list:
    publish_date_after = publish_date_after + 'T00:00:00Z'  # formatting the publish date after
    publish_date_before = publish_date_before + 'T00:00:00Z'  # formatting the publish date before

    video_ids = []  # A list for appending the video ids

    x = requests.get(
        'https://www.googleapis.com/youtube/v3/search?key=AIzaSyDnIqoMPASXgKPkzxlcy4krIPOHtJOJ998&channel/videoId='
        + channel_id + '&part=snippet,id&order=date&publishedBefore=+' + publish_date_before + '&publishedAfter='
        + publish_date_after)  # getting the data of channel/video

    if 200 <= x.status_code <= 399:  # some basic validations
        values = json.loads(x.text)  # we will parse the text to json and json to dictionary
        num = len(values['items'])  # getting the length of items

        for i in range(0, num):
            try:
                video_ids.append(values['items'][i]['id']['videoId'])  # appending the ids to list
            except:
                video_ids = video_ids + []  # some basic validations
                continue
        return video_ids  # returning the video ids
    else:
        return video_ids  # empty list if any error occurs


def get_subtitles(video_ids):
    texts = ''  # adding the subtitles
    no_subtitles = ''  # adding the ids in which subtitles settings are not proper
    error = ''  # A error text

    for video_id in video_ids:
        try:  # basic validations
            transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)  # fetching the transcript list
        except:
            no_subtitles = no_subtitles + " " + video_id  # adding the ids in which subtitles settings are not proper
            continue

        for transcript in transcript_list:
            contents = transcript.translate('en').fetch()  # translate the transcript into english
            for content in contents:
                texts = texts + content['text']  # adding the subtitles text to texts variable
                texts = texts + " "

    if len(no_subtitles) > 0:  # basic validations for subtitles settings
        error = 'Please check the subtitles setting of this particular video ids as they are skipped' + no_subtitles
    return texts, error  # returning the text and error


def get_clean_data(texts: AnyStr) -> AnyStr:
    texts = texts.lower()  # this function converts text to lower case
    texts = texts.replace(r"(http|@)\S+", "")  # Removing unnecessary stuff
    texts = texts.replace(r"::", ": :")  # Removing unnecessary stuff
    texts = texts.replace(r"’", "'")  # Removing unnecessary stuff
    texts = texts.replace(r"[^a-z\':_]", " ")  # Removing unnecessary stuff
    pattern = re.compile(r"(.)\1{2,}", re.DOTALL)  # Removing duplicates
    pattern = str(pattern)
    texts = texts.replace(pattern, r"\1")  # Removing unnecessary stuff and setting proper stuff instead
    texts = texts.replace(r"(can't|cannot)", 'can not')  # Removing unnecessary stuff and setting proper stuff instead
    texts = texts.replace(r"n't", ' not')  # Removing unnecessary stuff and setting proper stuff instead
    stopwords = nltk.corpus.stopwords.words('english')  # getting the stopwords
    stopwords.remove('not')  # removing some negations important which are for predictions
    stopwords.remove('nor')  # removing some negations important which are for predictions
    stopwords.remove('no')  # removing some negations important which are for predictions
    texts = ' '.join([word for word in texts.split() if word not in stopwords])  # removing stopwords from main texts
    return texts  # returning the clean text


@login_required(login_url='/users/login')  # Checking if the user is authenticated
def show_intent(request: AnyStr) -> Any:
    channel_id = request.POST.get('channel_id')  # Getting the channel/video id from the form using post method
    publish_date_after = request.POST.get(
        'publish_date_after')  # Getting the publish_date_after from the form using post method
    publish_date_before = request.POST.get(
        'publish_date_before')  # Getting the publish_date_before from the form using post method

    video_ids = get_youtube_data(channel_id, publish_date_after,
                                 publish_date_before)  # Getting the video ids using get_youtube_data method
    if len(video_ids) == 0:  # Some basic validations
        messages.error(request,
                       'Services are not working properly or invalid data')  # adding the errors in messages list which will be shown in message.html template
        return HttpResponseRedirect(
            reverse('sentiment:show_intent'))  # Redirecting to form page if there are any errors.

    texts, error_ = get_subtitles(video_ids)  # Getting the subtitles using get_subtitles method
    if texts == '':  # Some basic validations
        messages.error(request,
                       'Please check the subtitles setting of your channel/video')  # adding the errors in messages list which will be shown in message.html template
        return HttpResponseRedirect(
            reverse('sentiment:show_intent'))  # Redirecting to form page if there are any errors.
    if len(error_) > 0:  # Some basic validations
        messages.error(request,
                       error_)  # adding the errors in messages list which will be shown in message.html template

    texts = get_clean_data(texts)  # Getting the cleaned text using get_clean_data method

    predictions = predictor_intent.predict(texts, return_proba=True)  # predicting on the cleaned text
    labels = predictor_intent.get_classes()  # getting the labels

    intent = []  # empty list for labels
    intent_probabilities = []  # empty list for probabilities
    intents = {}  # A dict for labels and probabilities

    iterator = 0  # initializing a iterator to 0

    for prediction in predictions:  # appending different probabilities of predictions in x and y
        intents[labels[iterator]] = prediction  # appending everything to dict
        iterator = iterator + 1  # incrementing iterator

    intents = OrderedDict(sorted(intents.items(), key=itemgetter(1)))  # sorting the dict with respect to values

    iterator = 0  # re-initializing a iterator to 0

    for key in intents.keys():
        if iterator >= 147:
            intent.append(key)  # appending the labels to main intent list
            intent_probabilities.append(intents[key])  # appending the probabilities to main intent_probabilities list
        iterator = iterator + 1  # incrementing iterator

    context = {  # setting the context with our data
        'labels': intent,
        'probabilities': intent_probabilities,
    }
    return render(request, 'sentiment/results_intent.html',
                  context=context)  # rendering template with out data using jinja template engine


@login_required(login_url='/users/login')  # Checking if the user is authenticated
def show_intent_video(request: AnyStr) -> Any:
    video_ids = request.POST.get('video_id')  # Getting the video id from the form using post method
    if video_ids is None:                     # Some basic validations
         return HttpResponseRedirect(
            reverse('sentiment:show_intent_video'))
    video_ids = video_ids.split(' ')  # converting string to list
    texts, error_ = get_subtitles(video_ids)  # Getting the subtitles using get_subtitles method
    if texts == '':  # Some basic validations
        messages.error(request,
                       'Please check the subtitles setting of your channel/video')  # adding the errors in messages list which will be shown in message.html template
        return HttpResponseRedirect(
            reverse('sentiment:show_intent_video'))  # Redirecting to form page if there are any errors.
    if len(error_) > 0:  # Some basic validations
        messages.error(request,
                       error_)  # adding the errors in messages list which will be shown in message.html template

    texts = get_clean_data(texts)  # Getting the cleaned text using get_clean_data method

    predictions = predictor_intent.predict(texts, return_proba=True)  # predicting on the cleaned text
    labels = predictor_intent.get_classes()  # getting the labels

    intent = []  # empty list for labels
    intent_probabilities = []  # empty list for probabilities
    intents = {}  # A dict for labels and probabilities

    iterator = 0  # initializing a iterator to 0

    for prediction in predictions:  # appending different probabilities of predictions in x and y
        intents[labels[iterator]] = prediction  # appending everything to dict
        iterator = iterator + 1  # incrementing iterator

    intents = OrderedDict(sorted(intents.items(), key=itemgetter(1)))  # sorting the dict with respect to values

    iterator = 0  # re-initializing a iterator to 0

    for key in intents.keys():
        if iterator >= 147:
            intent.append(key)  # appending the labels to main intent list
            intent_probabilities.append(intents[key])  # appending the probabilities to main intent_probabilities list
        iterator = iterator + 1  # incrementing iterator

    context = {  # setting the context with our data
        'labels': intent,
        'probabilities': intent_probabilities,
    }
    return render(request, 'sentiment/results_intent.html',
                  context=context)  # rendering template with out data using jinja template engine


@login_required(login_url='/users/login')  # Checking if the user is authenticated
def show_emotion_video(request: AnyStr) -> Any:
    video_ids = request.POST.get('video_id')  # Getting the video id from the form using post method
    if video_ids is None:                     # Some basic validations
        return HttpResponseRedirect(
            reverse('sentiment:show_emotion_video'))
    video_ids = video_ids.split(' ')  # converting string to list
    texts, error_ = get_subtitles(video_ids)  # Getting the subtitles using get_subtitles method
    if texts == '':  # Some basic validations
        messages.error(request,
                       'Please check the subtitles setting of your channel/video')  # adding the errors in messages list which will be shown in message.html template
        return HttpResponseRedirect(
            reverse('sentiment:show_emotion_video'))  # Redirecting to form page if there are any errors
    if len(error_) > 0:  # Some basic validations
        messages.error(request,
                       error_)  # adding the errors in messages list which will be shown in message.html template

    texts = get_clean_data(texts)  # Getting the cleaned text using get_clean_data method

    emotion_predictions = predictor_emotion.predict(texts, return_proba=True)  # predicting on the cleaned text
    emotion_labels = predictor_emotion.get_classes()  # getting the labels

    context = {  # setting the context with our data
        'labels': emotion_labels,
        'probabilities': emotion_predictions,
    }
    return render(request, 'sentiment/results_emotion.html',
                  context=context)  # rendering template with out data using jinja template engine
