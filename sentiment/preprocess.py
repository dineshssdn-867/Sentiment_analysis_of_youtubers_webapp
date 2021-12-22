import re  # Importing re module for cleaning data
import nltk  # Importing nltk module for cleaning data and removing stopwords
from typing import AnyStr
from nltk import WordNetLemmatizer

wnl = WordNetLemmatizer()

def get_clean_data(texts: AnyStr) -> AnyStr:
    emoji_pattern = re.compile("["
                               u"\U0001F600-\U0001F64F"  # emoticons
                               u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                               u"\U0001F680-\U0001F6FF"  # transport & map symbols
                               u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                               "]+", flags=re.UNICODE)
    texts = emoji_pattern.sub(r'', texts)
    texts = texts.lower()  # this function converts text to lower case
    texts = texts.replace(r'https?:\/\/\S+', "")  # Removing unnecessary stuff
    texts = texts.replace(r'www\.[a - z]?\.?(com) + | [a - z] +\.(com)', "")  # Removing unnecessary stuff
    texts = texts.replace(r'{link}', "")  # Removing unnecessary stuff
    texts = texts.replace(r'\[video\]', "")  # Removing unnecessary stuff
    texts = texts.replace(r'\[Applause\]', "")  # Removing unnecessary stuff
    texts = texts.replace(r'\[Music\]', "")  # Removing unnecessary stuff
    texts = texts.replace(r'&[a-z]+;', "")  # Removing unnecessary stuff
    texts = texts.replace(r'\S*@\S*\s?', "")  # Removing unnecessary stuff
    texts = texts.replace(r"[^a-z\s\(\-:\)\\\/\];='#]", ": :")  # Removing unnecessary stuff
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
    texts = ' '.join([wnl.lemmatize(word) for word in texts.split() if word not in stopwords])  # removing stopwords from main texts
    return texts  # returning the clean text
