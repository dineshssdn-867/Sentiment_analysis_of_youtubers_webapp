from urllib import parse
import re


def get_video_id(url):
    url_parsed = parse.urlparse(url)
    qsl = parse.parse_qs(url_parsed.query)
    try:
        v = qsl['v'][0]
    except:
        match = re.search(r"(?:v=|\/)([0-9A-Za-z_-]{11}).*", url)
        if match:
            v = match.group(1)
        else:
            v = ""
    return v
