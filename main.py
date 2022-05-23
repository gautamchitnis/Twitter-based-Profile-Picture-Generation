import json
import requests
import pandas as pd
from utils.Cleaner import Cleaner

if __name__ == '__main__':
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

    cleaner = Cleaner()

    df = cleaner.clean_up(df)

    processed_count = 0
    max_count = 0

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
