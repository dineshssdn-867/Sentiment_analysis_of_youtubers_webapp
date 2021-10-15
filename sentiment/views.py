from collections import OrderedDict  # Importing ordered dict for sorting the dictionary data
from operator import itemgetter  # Importing item getter for getting the value for key in the dictionary data
from typing import Any, AnyStr  # Using to define the type
import json
import requests
from django.contrib import messages  # Importing messages module for showing errors
from django.contrib.auth.decorators import login_required  # Importing decorator for verifying the authenticated user
from django.http import HttpResponseRedirect  # If any error caused it will help to redirect
from django.shortcuts import render  # Jinja template engine will parse the contents using render
from django.urls import reverse  # Used in redirecting
from django.views.generic.base import TemplateView  # Importing template class based views
from .youtube import get_youtube_comment_data, get_clean_data, get_subtitles, get_youtube_data
from decouple import config

API = config('API')

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


class FormCommentViewVideoEmotion(TemplateView):  # Initializing template for template view
    template_name = 'sentiment/sentiment_form_emotion_comment_video.html'


class FormCommentViewVideoIntent(TemplateView):  # Initializing template for template view
    template_name = 'sentiment/sentiment_intent_form_video_comment.html'


@login_required(login_url='/users/login')  # Checking if the user is authenticated
def show_emotion(request: AnyStr) -> Any:
    channel_id = request.POST.get('channel_id')  # Getting the channel/video id from the form using post method
    publish_date_after = request.POST.get(
        'publish_date_after')  # Getting the publish_date_after from the form using post method
    publish_date_before = request.POST.get(
        'publish_date_before')  # Getting the publish_date_before from the form using post method
    video_ids = get_youtube_data(channel_id, publish_date_after,
                                 publish_date_before)  # Getting the video ids using get_youtube_data method

    if channel_id is None or publish_date_before is None or publish_date_after is None:
        return HttpResponseRedirect(reverse('sentiment:show_emotion'))

    if len(video_ids) == 0:  # Some basic validations
        messages.error(request,
                       'Services are not working properly or invalid data')  # adding the errors in messages list which will be shown in message.html template
        return HttpResponseRedirect(
            reverse('sentiment:show_emotion'))  # Redirecting to form page if there are any errors.

    texts, error_ = get_subtitles(video_ids)  # Getting the subtitles using get_subtitles method
    texts = "I am happy"
    if texts == '':  # Some basic validations
        messages.error(request,
                       'Please check the subtitles setting of your channel/video')  # adding the errors in messages list which will be shown in message.html template
        return HttpResponseRedirect(
            reverse('sentiment:show_emotion'))  # Redirecting to form page if there are any errors

    if len(error_) > 0:  # Some basic validations
        messages.error(request,
                       error_)  # adding the errors in messages list which will be shown in message.html template

    texts = get_clean_data(texts)  # Getting the cleaned text using get_clean_data method
    emotion_predictions = requests.post(API+'emotion', json={"text":texts})
    emotion_labels = emotion_predictions.json()['emotion_labels']  # getting the labels
    emotion_predictions=emotion_predictions.json()['emotion_predictions']

    context = {  # setting the context with our data
        'labels': emotion_labels,
        'probabilities': emotion_predictions,
    }
    return render(request, 'sentiment/results_emotion.html',
                  context=context)  # rendering template with out data using jinja template engine


@login_required(login_url='/users/login')  # Checking if the user is authenticated
def show_intent(request: AnyStr) -> Any:
    channel_id = request.POST.get('channel_id')  # Getting the channel/video id from the form using post method
    publish_date_after = request.POST.get(
        'publish_date_after')  # Getting the publish_date_after from the form using post method
    publish_date_before = request.POST.get(
        'publish_date_before')  # Getting the publish_date_before from the form using post method

    if channel_id is None or publish_date_before is None or publish_date_after is None:
        return HttpResponseRedirect(reverse('sentiment:show_emotion'))

    video_ids = get_youtube_data(channel_id, publish_date_after,
                                 publish_date_before)  # Getting the video ids using get_youtube_data method
    if len(video_ids) == 0:  # Some basic validations
        messages.error(request,
                       'Services are not working properly or invalid data')  # adding the errors in messages list
        # which will be shown in message.html template
        return HttpResponseRedirect(
            reverse('sentiment:show_intent'))  # Redirecting to form page if there are any errors.

    texts, error_ = get_subtitles(video_ids)  # Getting the subtitles using get_subtitles method
    if texts == '':  # Some basic validations
        messages.error(request,
                       'Please check the subtitles setting of your channel/video')  # adding the errors in messages
        # list which will be shown in message.html template
        return HttpResponseRedirect(
            reverse('sentiment:show_intent'))  # Redirecting to form page if there are any errors.
    if len(error_) > 0:  # Some basic validations
        messages.error(request,
                       error_)  # adding the errors in messages list which will be shown in message.html template

    texts = get_clean_data(texts)  # Getting the cleaned text using get_clean_data method

    intent_predictions = requests.post(API+'intent', json={"text":texts})
    labels = intent_predictions.json()['intent_labels']  # getting the labels
    intent_predictions=intent_predictions.json()['intent_predictions']

    context = {  # setting the context with our data
        'labels': labels,
        'probabilities': intent_predictions,
    }
    return render(request, 'sentiment/results_intent.html',
                  context=context)  # rendering template with out data using jinja template engine


@login_required(login_url='/users/login')  # Checking if the user is authenticated
def show_intent_video(request: AnyStr) -> Any:
    video_ids = request.POST.get('video_id')  # Getting the video id from the form using post method
    if video_ids is None:  # Some basic validations
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

    intent_predictions = requests.post(API+'intent', json={"text":texts})
    labels = intent_predictions.json()['intent_labels']  # getting the labels
    intent_predictions=intent_predictions.json()['intent_predictions']

    context = {  # setting the context with our data
        'labels': labels,
        'probabilities': intent_predictions,
    }
    return render(request, 'sentiment/results_intent.html',
                  context=context)  # rendering template with out data using jinja template engine


@login_required(login_url='/users/login')  # Checking if the user is authenticated
def show_emotion_video(request: AnyStr) -> Any:
    video_ids = request.POST.get('video_id')  # Getting the video id from the form using post method
    if video_ids is None:  # Some basic validations
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

    emotion_predictions = requests.post(API+'emotion', json={"text":texts})
    emotion_labels = emotion_predictions.json()['emotion_labels']  # getting the labels
    emotion_predictions=emotion_predictions.json()['emotion_predictions']

    context = {  # setting the context with our data
        'labels': emotion_labels,
        'probabilities': emotion_predictions,
    }
    return render(request, 'sentiment/results_emotion.html',
                  context=context)  # rendering template with out data using jinja template engine


@login_required(login_url='/users/login')  # Checking if the user is authenticated
def show_comment_intent_video(request: AnyStr) -> Any:
    video_id = request.POST.get('video_id')  # Getting the video id from the form using post method
    if video_id is None:  # Some basic validations
        return HttpResponseRedirect(
            reverse('sentiment:show_intent_video'))
    texts = get_youtube_comment_data(video_id)  # Getting the subtitles using get_subtitles method
    if texts == '':  # Some basic validations
        messages.error(request,
                       'Please check the subtitles setting of your channel/video')  # adding the errors in messages list which will be shown in message.html template
        return HttpResponseRedirect(
            reverse('sentiment:show_intent_video'))  # Redirecting to form page if there are any errors.

    intent_predictions = requests.post(API+'intent', json={"text":texts})
    labels = intent_predictions.json()['intent_labels']  # getting the labels
    intent_predictions=intent_predictions.json()['intent_predictions']

    context = {  # setting the context with our data
        'labels': labels,
        'probabilities': intent_predictions,
    }
    return render(request, 'sentiment/results_intent.html',
                  context=context)  # rendering template with out data using jinja template engine


@login_required(login_url='/users/login')  # Checking if the user is authenticated
def show_comment_emotion_video(request: AnyStr) -> Any:
    video_id = request.POST.get('video_id')  # Getting the video id from the form using post method
    if video_id is None:  # Some basic validations
        return HttpResponseRedirect(
            reverse('sentiment:show_emotion_video'))
    texts = get_youtube_comment_data(video_id)  # Getting the subtitles using get_subtitles method
    if texts == '':  # Some basic validations
        messages.error(request,
                       'Please check the subtitles setting of your channel/video')  # adding the errors in messages list which will be shown in message.html template
        return HttpResponseRedirect(
            reverse('sentiment:show_emotion_video'))  # Redirecting to form page if there are any errors

    emotion_predictions = requests.post(API+'emotion', json={"text":texts})
    emotion_labels = emotion_predictions.json()['emotion_labels']  # getting the labels
    emotion_predictions=emotion_predictions.json()['emotion_predictions']


    context = {  # setting the context with our data
        'labels': emotion_labels,
        'probabilities': emotion_predictions,
    }
    return render(request, 'sentiment/results_emotion.html',
                  context=context)  # rendering template with out data using jinja template eng
