import tweepy
from utils.Auth import Auth
import pandas as pd


class TWManager:
    api = None

    def __init__(self):
        auth = Auth()
        auth.set_auth_keys()
        self.api = auth.get_auth()

    def find_user(self, username):
        try:
            user = self.api.lookup_users(screen_name=[username])
            return user
        except Exception as e:
            print(e)

    def tweets_df_by_user(self, username):
        count = 0
        # max_count = 4000
        page_count = 0

        df = pd.DataFrame()
        rows = [df]

        for page in tweepy.Cursor(
                self.api.user_timeline,
                screen_name=username,
                trim_user=True,
                # exclude_replies=True,
                # include_rts=False,
                count=10
        ).pages(10):
            page_count += 1
            print(f"Processing page {page_count}:")
            for tweet in page:
                count += 1
                rows.append(pd.DataFrame([[tweet.id, tweet.author.id, tweet.text]], columns=['tweet_id', 'author_id', 'text']))
                print(f"Received {count} tweets.")

        df = pd.concat(rows, ignore_index=True)
        df.transpose()
        return df
