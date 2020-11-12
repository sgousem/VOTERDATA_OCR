import os
#import pickle
#import const
import requests

def transliterate(text, l1, l2):
    response = requests.get(
        "https://inputtools.google.com/request",
        params={
            "text": text,
            "ime": "_".join(['transliteration', l1, l2]),
            "ie": "utf-8",
            "oe": "utf-8",
            "app": "jsapi",
        }
    )
    if not response.ok:
        return False
    jc = response.json()
    if jc[0] != 'SUCCESS':
        return
    try:
        result = jc[-1][0][1][0]
    except:
        result = text
    return result

def transliterate_tel(eng_text):
    eng_text = eng_text.replace(':', '')
    return transliterate(eng_text, 'en', 'te')
def transliterate_ass(ass_text):
    ass_text = ass_text.replace(':', '')
    return transliterate(ass_text, 'bn', 'en')

def transliterate_hin(hindi_text):
    hindi_text = hindi_text.replace(':', '')
    return transliterate(hindi_text, 'hi', 'en')


print(transliterate_ass("পুৰুষ"))