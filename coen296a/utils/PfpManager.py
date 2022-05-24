import json
import requests


class PicMaker:
    url = ""

    def __init__(self, url):
        self.url = url

    def generate_image_from_df(self, df):
        tokens = []

        for index, row in df.iterrows():
            tokens.extend(row['lemma_tokens'])

        tokens = list(set(tokens))

        tweet_topics = ",".join(tokens)
        payload = json.dumps({
            "prompt": tweet_topics
        })

        headers = {
            'Content-Type': 'application/json'
        }

        response = requests.request("POST", self.url, headers=headers, data=payload)

        # with open("response.png", "wb") as f:
        #     f.write(response.content)
        return response.content