import re  # Importing re module for cleaning data
import nltk  # Importing nltk module for cleaning data and removing stopwords
from typing import AnyStr


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
