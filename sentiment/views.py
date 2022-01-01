from typing import Any, AnyStr  # Using to define the type
import requests
from django.contrib import messages  # Importing messages module for showing errors
from django.contrib.auth.decorators import login_required  # Importing decorator for verifying the authenticated user
from django.http import HttpResponseRedirect  # If any error caused it will help to redirect
from django.shortcuts import render  # Jinja template engine will parse the contents using render
from django.urls import reverse  # Used in redirecting
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_headers
from django.views.generic.base import TemplateView  # Importing template class based views
from .youtube import get_youtube_comment_data, get_clean_data, get_subtitles, get_youtube_data, get_channel_id
from decouple import config
from .api import analyze_emotion
from .sentiments import sentiment_analysis
from .retrieve_data import get_video_id

API = config('API')


# @method_decorator(vary_on_headers('User-Agent', 'Cookie'), name='dispatch')
# @method_decorator(cache_page(int(60 * .167), cache="cache1"), name='dispatch')
class HomeView(TemplateView):  # Initializing template for template view
    template_name = 'sentiment/index.html'


@method_decorator(vary_on_headers('User-Agent', 'Cookie'), name='dispatch')
@method_decorator(cache_page(int(60 * .167), cache="cache1"), name='dispatch')
class FormViewSentiment(TemplateView):  # Initializing template for template view
    template_name = 'sentiment/sentiment_sentiment_form.html'


@method_decorator(vary_on_headers('User-Agent', 'Cookie'), name='dispatch')
@method_decorator(cache_page(int(60 * .167), cache="cache1"), name='dispatch')
class FormViewVideoSentiment(TemplateView):  # Initializing template for template view
    template_name = 'sentiment/sentiment_form_sentiment_video.html'


@method_decorator(vary_on_headers('User-Agent', 'Cookie'), name='dispatch')
@method_decorator(cache_page(int(60 * .167), cache="cache1"), name='dispatch')
class FormCommentViewVideoSentiment(TemplateView):  # Initializing template for template view
    template_name = 'sentiment/sentiment_form_sentiment_comment_video.html'


@method_decorator(vary_on_headers('User-Agent', 'Cookie'), name='dispatch')
@method_decorator(cache_page(int(60 * .167), cache="cache1"), name='dispatch')
class FormViewEmotion(TemplateView):  # Initializing template for template view
    template_name = 'sentiment/sentiment_emotion_form.html'


@method_decorator(vary_on_headers('User-Agent', 'Cookie'), name='dispatch')
@method_decorator(cache_page(int(60 * .167), cache="cache1"), name='dispatch')
class FormViewVideoEmotion(TemplateView):  # Initializing template for template view
    template_name = 'sentiment/sentiment_form_emotion_video.html'


@method_decorator(vary_on_headers('User-Agent', 'Cookie'), name='dispatch')
@method_decorator(cache_page(int(60 * .167), cache="cache1"), name='dispatch')
class FormCommentViewVideoEmotion(TemplateView):  # Initializing template for template view
    template_name = 'sentiment/sentiment_form_emotion_comment_video.html'


@login_required(login_url='/users/login/')  # Checking if the user is authenticated
def show_emotion(request: AnyStr) -> Any:
    channel_name = request.POST.get('channel name')  # Getting the channel/video id from the form using post method
    publish_date_after = request.POST.get(
        'publish_date_after')  # Getting the publish_date_after from the form using post method
    publish_date_before = request.POST.get(
        'publish_date_before')  # Getting the publish_date_before from the form using post method

    channel_id = get_channel_id(channel_name)

    if channel_id is None:
        messages.error(request,
                       'Sorry channel does not exists')  # adding the errors in messages list which will be shown in message.html template
        return HttpResponseRedirect(
            reverse('sentiment:show_emotion'))

    if publish_date_before is None or publish_date_after is None:
        return HttpResponseRedirect(reverse('sentiment:show_emotion'))

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

    emotion_predictions = analyze_emotion(texts)
    emotion_labels = emotion_predictions['emotion_labels']  # getting the labels
    emotion_predictions = emotion_predictions['emotion_predictions']  # getting the probabilities

    context = {  # setting the context with our data
        'labels': emotion_labels,
        'probabilities': emotion_predictions,
    }

    return render(request, 'sentiment/results_emotion.html',
                  context=context)  # rendering template with out data using jinja template engine


@login_required(login_url='/users/login/')  # Checking if the user is authenticated
def show_emotion_video(request: AnyStr) -> Any:
    url = request.POST.get('url')  # Getting the video id from the form using post method
    if url is None:  # Some basic validations
        messages.error(request,
                       'Please check the url you entered')
        return HttpResponseRedirect(
            reverse('sentiment:show_emotion_video'))
    video_ids = get_video_id(url)
    if video_ids is None:  # Some basic validations
        messages.error(request,
                       'Please check the url you entered')
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

    emotion_predictions = analyze_emotion(texts)
    emotion_labels = emotion_predictions['emotion_labels']  # getting the labels
    emotion_predictions = emotion_predictions['emotion_predictions']  # getting the probabilities

    context = {  # setting the context with our data
        'labels': emotion_labels,
        'probabilities': emotion_predictions,
    }
    return render(request, 'sentiment/results_emotion.html',
                  context=context)  # rendering template with out data using jinja template engine


@login_required(login_url='/users/login/')  # Checking if the user is authenticated
def show_comment_emotion_video(request: AnyStr) -> Any:
    url = request.POST.get('url')  # Getting the video id from the form using post method
    if url is None:  # Some basic validations
        messages.error(request,
                       'Please check the url you entered')
        return HttpResponseRedirect(
            reverse('sentiment:show_emotion_video_comment'))
    video_ids = get_video_id(url)
    if video_ids is None:  # Some basic validations
        messages.error(request,
                       'Please check the url you entered')
        return HttpResponseRedirect(
            reverse('sentiment:show_emotion_video_comment'))
    texts = get_youtube_comment_data(video_ids)  # Getting the subtitles using get_subtitles method
    if texts == '':  # Some basic validations
        messages.error(request,
                       'Please check whether the comments are disabled. Also, please check the url you entered.')  # adding the errors in messages list which will be shown in message.html template
        return HttpResponseRedirect(
            reverse('sentiment:show_emotion_video_comment'))  # Redirecting to form page if there are any errors

    if not (texts and not texts.isspace()):  # Some basic validations
        messages.error(request,
                       'Please check the comment settings or try after some time')  # adding the errors in messages list which will be shown in message.html template
        return HttpResponseRedirect(
            reverse('sentiment:show_emotion_video_comment'))  # Redirecting to form page if there are any errors.
    emotion_predictions = analyze_emotion(texts)
    emotion_labels = emotion_predictions['emotion_labels']  # getting the labels
    emotion_predictions = emotion_predictions['emotion_predictions']  # getting the probabilities

    context = {  # setting the context with our data
        'labels': emotion_labels,
        'probabilities': emotion_predictions,
    }
    return render(request, 'sentiment/results_emotion.html',
                  context=context)  # rendering template with out data using jinja template eng


@login_required(login_url='/users/login/')  # Checking if the user is authenticated
def show_sentiment(request: AnyStr) -> Any:
    channel_name = request.POST.get('channel name')  # Getting the channel/video id from the form using post method
    publish_date_after = request.POST.get(
        'publish_date_after')  # Getting the publish_date_after from the form using post method
    publish_date_before = request.POST.get(
        'publish_date_before')  # Getting the publish_date_before from the form using post method

    channel_id = get_channel_id(channel_name)

    if channel_id is None:
        messages.error(request,
                       'Sorry channel does not exists')  # adding the errors in messages list which will be shown in message.html template
        return HttpResponseRedirect(
            reverse('sentiment:show_sentiment'))

    if publish_date_before is None or publish_date_after is None:
        return HttpResponseRedirect(reverse('sentiment:show_sentiment'))

    video_ids = get_youtube_data(channel_id, publish_date_after,
                                 publish_date_before)  # Getting the video ids using get_youtube_data method

    if len(video_ids) == 0:  # Some basic validations
        messages.error(request,
                       'Services are not working properly or invalid data')  # adding the errors in messages list which will be shown in message.html template
        return HttpResponseRedirect(
            reverse('sentiment:show_sentiment'))  # Redirecting to form page if there are any errors.

    texts, error_ = get_subtitles(video_ids)  # Getting the subtitles using get_subtitles method
    if texts == '':  # Some basic validations
        messages.error(request,
                       'Please check the subtitles setting of your channel/video')  # adding the errors in messages list which will be shown in message.html template
        return HttpResponseRedirect(
            reverse('sentiment:show_sentiment'))  # Redirecting to form page if there are any errors

    if len(error_) > 0:  # Some basic validations
        messages.error(request,
                       error_)  # adding the errors in messages list which will be shown in message.html template

    texts = get_clean_data(texts)  # Getting the cleaned text using get_clean_data method

    emotion_predictions, emotion_labels, subjectivity = sentiment_analysis(texts)

    if emotion_predictions is None or emotion_labels is None or subjectivity['subjectivity'] == '':
        messages.error(request,
                       'We are a facing some issue. Please try again later')  # adding the errors in messages list which will be shown in message.html template
        return HttpResponseRedirect(
            reverse('sentiment:show_sentiment'))  # Redirecting to form page if there are any errors.

    context = {  # setting the context with our data
        'labels': emotion_labels,
        'probabilities': emotion_predictions,
        'subjectivity': subjectivity['subjectivity']
    }

    return render(request, 'sentiment/results_sentiment.html',
                  context=context)  # rendering template with out data using jinja template engine


@login_required(login_url='/users/login/')  # Checking if the user is authenticated
def show_sentiment_video(request: AnyStr) -> Any:
    url = request.POST.get('url')  # Getting the video id from the form using post method
    if url is None:  # Some basic validations
        messages.error(request,
                       'Please check the url you entered')
        return HttpResponseRedirect(
            reverse('sentiment:show_sentiment_video'))
    video_ids = get_video_id(url)
    if video_ids is None:  # Some basic validations
        messages.error(request,
                       'Please check the url you entered')
        return HttpResponseRedirect(
            reverse('sentiment:show_sentiment_video'))
    video_ids = video_ids.split(' ')  # converting string to list
    texts, error_ = get_subtitles(video_ids)  # Getting the subtitles using get_subtitles method
    if texts == '':  # Some basic validations
        messages.error(request,
                       'Please check the subtitles setting of your channel/video')  # adding the errors in messages list which will be shown in message.html template
        return HttpResponseRedirect(
            reverse('sentiment:show_sentiment_video'))  # Redirecting to form page if there are any errors
    if len(error_) > 0:  # Some basic validations
        messages.error(request,
                       error_)  # adding the errors in messages list which will be shown in message.html template

    texts = get_clean_data(texts)  # Getting the cleaned text using get_clean_data method

    emotion_predictions, emotion_labels, subjectivity = sentiment_analysis(texts)

    if emotion_predictions is None or emotion_labels is None or subjectivity['subjectivity'] == '':
        messages.error(request,
                       'We are a facing some issue. Please try again later')  # adding the errors in messages list which will be shown in message.html template
        return HttpResponseRedirect(
            reverse('sentiment:show_sentiment_video'))  # Redirecting to form page if there are any errors.

    context = {  # setting the context with our data
        'labels': emotion_labels,
        'probabilities': emotion_predictions,
        'subjectivity': subjectivity['subjectivity']
    }

    return render(request, 'sentiment/results_sentiment.html',
                  context=context)  # rendering template with out data using jinja template engine


@login_required(login_url='/users/login/')  # Checking if the user is authenticated
def show_comment_sentiment_video(request: AnyStr) -> Any:
    url = request.POST.get('url')  # Getting the video id from the form using post method
    if url is None:  # Some basic validations
        messages.error(request,
                       'Please check the url you entered')
        return HttpResponseRedirect(
            reverse('sentiment:show_sentiment_video_comment'))
    video_ids = get_video_id(url)
    if video_ids is None:  # Some basic validations
        messages.error(request,
                       'Please check the url you entered')
        return HttpResponseRedirect(
            reverse('sentiment:show_sentiment_video_comment'))
    texts = get_youtube_comment_data(video_ids)  # Getting the subtitles using get_subtitles method
    if texts == '':  # Some basic validations
        messages.error(request,
                       'Please check whether the comments are disabled. Also, please check the url you entered.')  # adding the errors in messages list which will be shown in message.html template
        return HttpResponseRedirect(
            reverse('sentiment:show_sentiment_video_comment'))  # Redirecting to form page if there are any errors

    if not (texts and not texts.isspace()):  # Some basic validations
        messages.error(request,
                       'Please check the comment settings or try after some time')  # adding the errors in messages list which will be shown in message.html template
        return HttpResponseRedirect(
            reverse('sentiment:show_sentiment_video_comment'))  # Redirecting to form page if there are any errors.

    emotion_predictions, emotion_labels, subjectivity = sentiment_analysis(texts)

    if emotion_predictions is None or emotion_labels is None or subjectivity['subjectivity'] == '':
        messages.error(request,
                       'We are a facing some issue. Please try again later')  # adding the errors in messages list which will be shown in message.html template
        return HttpResponseRedirect(
            reverse('sentiment:show_sentiment_video_comment'))  # Redirecting to form page if there are any errors.

    context = {  # setting the context with our data
        'labels': emotion_labels,
        'probabilities': emotion_predictions,
        'subjectivity': subjectivity['subjectivity']
    }

    return render(request, 'sentiment/results_sentiment.html',
                  context=context)  # rendering template with out data using jinja template eng
