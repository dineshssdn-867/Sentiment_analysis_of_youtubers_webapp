from urllib import parse


def get_video_id(url):
    url_parsed = parse.urlparse(url)
    qsl = parse.parse_qs(url_parsed.query)
    try:
        v = qsl['v'][0]
    except:
        v = ''
    return v
