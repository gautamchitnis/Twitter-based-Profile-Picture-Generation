import spacy
from spacy import Language
from spacy.tokenizer import Tokenizer
import re
import string
import emoji.core as emoji
from spacy_langdetect import LanguageDetector
from wordcloud import STOPWORDS


@Language.factory("language_detector")
def create_language_detector(nlp, name):
    return LanguageDetector(language_detection_function=None)


class Cleaner:

    nlp = None

    def __init__(self):
        self.nlp = spacy.load('en_core_web_lg')

    def remove_emoji(self, text):
        text = emoji.replace_emoji(text, '')
        return text

    def remove_url(self, text):
        text = re.sub(r'http\S+', '', text)
        return text

    def get_lemmas(self, text):
        lemmas = []
        doc = self.nlp(text)
        for token in doc:
            if ((token.is_stop == False) and (token.is_punct == False)) and (token.pos_ != 'PRON'):
                if token._.language["language"] == 'en' or token._.language["score"] < 0.8:
                    lemmas.append(token.lemma_)

        return lemmas

    # Tokenizer function
    def tokenize(self, text):
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

    def clean_up(self, df):
        # TODO: see if its possible to detect words with different lang chars and only discard them instead of discarding based on lang det

        df['emoji_free_tweet'] = df['text'].apply(self.remove_emoji)
        df['url_free_tweet'] = df['emoji_free_tweet'].apply(self.remove_url)

        self.nlp.add_pipe('language_detector')

        # Tokenizer
        tokenizer = Tokenizer(self.nlp.vocab)

        # Custom stopwords
        custom_stopwords = ['hi', '\n', '\n\n', '&amp;', ' ', '.', '-', 'got', "it's", 'it’s', "i'm", 'i’m', 'im',
                            'want',
                            'like', '$', '@', 'rt']

        # Customize stop words by adding to the default list
        STOP_WORDS = self.nlp.Defaults.stop_words.union(custom_stopwords)
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

        df['lemmas'] = df['tokens_back_to_text'].apply(self.get_lemmas)

        # Make lemmas a string again
        df['lemmas_back_to_text'] = [' '.join(map(str, l)) for l in df['lemmas']]

        # Apply tokenizer
        df['lemma_tokens'] = df['lemmas_back_to_text'].apply(self.tokenize)
        return df
