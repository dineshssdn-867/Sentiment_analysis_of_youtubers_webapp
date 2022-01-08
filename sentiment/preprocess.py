import re  # Importing re module for cleaning data
from typing import AnyStr


def get_clean_data(texts: AnyStr) -> AnyStr:
    emoji_pattern = re.compile("["
                               u"\U0001F600-\U0001F64F"  # emoticons
                               u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                               u"\U0001F680-\U0001F6FF"  # transport & map symbols
                               u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                               "]+", flags=re.UNICODE)
    texts = emoji_pattern.sub(r'', texts)
    regex = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
    texts = re.sub(regex, '', texts, flags=re.MULTILINE)
    texts = re.sub('[^a-zA-Z]', ' ', texts)
    texts = texts.lower()  # this function converts text to lower case
    pattern = re.compile(r"(.)\1{2,}", re.DOTALL)  # Removing duplicates
    pattern = str(pattern)
    texts = texts.replace(pattern, r"\1")  # Removing unnecessary stuff and setting proper stuff instead
    texts = texts.replace(r"(can't|cannot)", 'can not')  # Removing unnecessary stuff and setting proper stuff instead
    texts = texts.replace(r"n't", ' not')  # Removing unnecessary stuff and setting proper stuff instead
    texts = re.sub(r'[^\w\s]', '', texts)
    return texts  # returning the clean text
