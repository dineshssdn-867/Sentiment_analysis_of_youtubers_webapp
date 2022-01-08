import concurrent.futures
from deep_translator import GoogleTranslator


def Translate(texts, language_check):
    translated = GoogleTranslator(source=language_check, target='en')
    text_translate = translated.translate(texts)
    return text_translate


def translate_multiprocess(texts, language_checks):
    with concurrent.futures.ThreadPoolExecutor(2) as executor:
        results = {executor.submit(Translate, texts[i], language_checks[i]): (texts[i], language_checks[i]) for i in
                   range(0, len(texts))}
        text_translate_multiprocess = ''
        for future in concurrent.futures.as_completed(results):
            text_translate_multiprocess = text_translate_multiprocess + ' ' + future.result()
    return text_translate_multiprocess
