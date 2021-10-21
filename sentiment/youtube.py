import json  # parsing the web data in python dicitionary
import requests  # Importing requests module for requesting the data from api
from youtube_transcript_api import \
    YouTubeTranscriptApi  # This library will help to fetch to subtitles of youtubers using the video ids
from translate import Translator
from typing import Any, AnyStr  # mentioning the types of data
from .preprocess import get_clean_data

translator = Translator(to_lang="English")


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


def get_youtube_comment_data(video_id: AnyStr) -> AnyStr:
    x = requests.get(
        'https://www.googleapis.com/youtube/v3/commentThreads?part=snippet&videoId=' + video_id + '&key=AIzaSyDnIqoMPASXgKPkzxlcy4krIPOHtJOJ998')  # getting the data of channel/video
    text = ''
    if 200 <= x.status_code <= 399:  # some basic validations
        values = json.loads(x.text)  # we will parse the text to json and json to dictionary
        num = len(values['items'])  # getting the length of items
        for i in range(0, num):
            try:
                text = text + values['items'][i]['snippet']["topLevelComment"]['snippet'][
                    'textOriginal'] + ' '  # appending the text to list
            except:
                text = text + ' '  # some basic validations
                continue
        text = get_clean_data(text)
        #text = translator.translate(text)
        return text  # returning the video ids
    else:
        return text  # empty list if any error occurs
