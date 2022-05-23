import json
import requests
# import pandas as pd
from utils.Cleaner import Cleaner
from utils.TWManager import TWManager

if __name__ == '__main__':
    url = "<URL>/index"

    twm = TWManager()
    df = twm.tweets_df_by_user("<USERNAME>")

    # df = pd.read_json(
    #     "data.json",
    #     orient='index',
    #     keep_default_dates=False,
    #     convert_dates=False,
    #     convert_axes=False
    # )
    #
    # df.reset_index(inplace=True)
    # df = df.rename(columns={'index': 'tweet_id'})

    cleaner = Cleaner()

    df = cleaner.clean_up(df)

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

    response = requests.request("POST", url, headers=headers, data=payload)

    with open("response.png", "wb") as f:
        f.write(response.content)
