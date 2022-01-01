from textblob import TextBlob


def sentiment_analysis(text):
    try:
        score = TextBlob(text).sentiment.polarity
        subjectivity = TextBlob(text).sentiment.subjectivity
    except:
        return [], [], {'subjectivity': ''}
    if score < 0:
        positive = 0
        negative = 1
        neutral = 0
        return [positive, negative, neutral], ['positive', 'negative', 'neutral'], {'subjectivity': subjectivity}
    elif score == 0:
        positive = 0
        negative = 0
        neutral = 1
        return [positive, negative, neutral], ['positive', 'negative', 'neutral'], {'subjectivity': subjectivity}
    else:
        positive = 1
        negative = 0
        neutral = 0
        return [positive, negative, neutral], ['positive', 'negative', 'neutral'], {'subjectivity': subjectivity}
