import json
import requests
import pandas as pd
# import numpy as np
import emoji.core as emoji
# import regex
import re
import string
# from collections import Counter

import spacy
from spacy.tokenizer import Tokenizer
from spacy.language import Language
from spacy.tokens import Doc, Span, Token
from spacy_langdetect import LanguageDetector
from wordcloud import STOPWORDS
from googletrans import Translator


def custom_detection_function(spacy_object):
    # custom detection function should take a Spacy Doc/Span/Token
    assert isinstance(spacy_object, Doc) or isinstance(
        spacy_object, Span) or isinstance(spacy_object, Token), "spacy_object must be a spacy Doc or Span object but it is a {}".format(type(spacy_object))
    detection = Translator().detect(spacy_object.text)
    return {'language': detection.lang, 'score': detection.confidence}


@Language.factory("language_detector")
def create_language_detector(nlp, name):
    return LanguageDetector(language_detection_function=None)


def remove_emoji(text):
    text = emoji.replace_emoji(text, '')
    return text


def remove_url(text):
    text = re.sub(r'http\S+', '', text)
    return text


def get_lemmas(text):
    lemmas = []
    doc = nlp(text)
    for token in doc:
        if ((token.is_stop == False) and (token.is_punct == False)) and (token.pos_ != 'PRON'):
            # if ((token.is_stop == False) and (token.is_punct == False) and (token._.language["language"] == 'en')) and (token.pos_ != 'PRON'):
            # if ((token.is_stop == False) and (token.is_punct == False) and (token.lang_ == 'en')) and (token.pos_ != 'PRON'):
            if token._.language["language"] == 'en' or token._.language["score"] < 0.8:
                lemmas.append(token.lemma_)

    return lemmas


# Tokenizer function
def tokenize(text):
    # Removing url's
    pattern = r"http\S+"

    tokens = re.sub(pattern, "", text)  # https://www.youtube.com/watch?v=O2onA4r5UaY
    tokens = re.sub('[^a-zA-Z 0-9]', '', text)
    tokens = re.sub('[%s]' % re.escape(string.punctuation), '', text)  # Remove punctuation
    tokens = re.sub('\w*\d\w*', '', text)  # Remove words containing numbers
    tokens = re.sub('@*!*\$*', '', text)  # Remove @ ! $
    tokens = tokens.strip(',')  # TESTING THIS LINE
    tokens = tokens.strip('?')  # TESTING THIS LINE
    tokens = tokens.strip('!')  # TESTING THIS LINE
    tokens = tokens.strip("'")  # TESTING THIS LINE
    tokens = tokens.strip(".")  # TESTING THIS LINE

    tokens = tokens.lower().split()  # Make text lowercase and split it

    return tokens


def clean_up(df):
    # TODO: see if its possible to detect words with different lang chars and only discard them instead of discarding based on lang det

    df['emoji_free_tweet'] = df['text'].apply(remove_emoji)
    df['url_free_tweet'] = df['emoji_free_tweet'].apply(remove_url)

    nlp.add_pipe('language_detector')

    # Tokenizer
    tokenizer = Tokenizer(nlp.vocab)

    # Custom stopwords
    custom_stopwords = ['hi', '\n', '\n\n', '&amp;', ' ', '.', '-', 'got', "it's", 'it’s', "i'm", 'i’m', 'im', 'want',
                        'like', '$', '@', 'rt']

    # Customize stop words by adding to the default list
    STOP_WORDS = nlp.Defaults.stop_words.union(custom_stopwords)
    stopwords = set(STOPWORDS)

    # ALL_STOP_WORDS = spacy + gensim + wordcloud
    # ALL_STOP_WORDS = STOP_WORDS.union(SW).union(stopwords)
    ALL_STOP_WORDS = STOP_WORDS.union(stopwords)

    tokens = []

    for doc in tokenizer.pipe(df['url_free_tweet'], batch_size=500):
        doc_tokens = []
        for token in doc:
            if token.text.lower() not in STOP_WORDS:
                doc_tokens.append(token.text.lower())
        tokens.append(doc_tokens)

    # Makes tokens column
    df['tokens'] = tokens

    # Make tokens a string again
    df['tokens_back_to_text'] = [' '.join(map(str, l)) for l in df['tokens']]

    df['lemmas'] = df['tokens_back_to_text'].apply(get_lemmas)

    # Make lemmas a string again
    df['lemmas_back_to_text'] = [' '.join(map(str, l)) for l in df['lemmas']]

    # Apply tokenizer
    df['lemma_tokens'] = df['lemmas_back_to_text'].apply(tokenize)
    return df


if __name__ == '__main__':
    nlp = spacy.load('en_core_web_lg')
    url = "<URL>/index"

    df = pd.read_json(
        "data.json",
        orient='index',
        keep_default_dates=False,
        convert_dates=False,
        convert_axes=False
    )

    df.reset_index(inplace=True)
    df = df.rename(columns={'index': 'tweet_id'})
    df = clean_up(df)

    processed_count = 0
    max_count = 1

    for index, row in df.iterrows():
        if processed_count != max_count:
            processed_count += 1

            tweet_topics = ",".join(row['lemma_tokens'])
            payload = json.dumps({
                "prompt": tweet_topics
            })

            headers = {
                'Content-Type': 'application/json'
            }

            response = requests.request("POST", url, headers=headers, data=payload)

            with open("response.png", "wb") as f:
                f.write(response.content)
