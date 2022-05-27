import tweepy
from utils.Auth import Auth
import pandas as pd


class TWManager:
    api = None
    auth = None

    def __init__(self):
        auth = Auth()
        auth.set_auth_keys()
        self.auth = auth
        self.api = auth.get_auth()

    def auth_user(self, tw_user):
        keys = self.auth.get_auth_keys()

        keys.access_token = tw_user.twitter_oauth_token.oauth_token
        keys.access_token_secret = tw_user.twitter_oauth_token.oauth_token_secret

        self.auth.set_auth_keys(keys=keys)
        self.api = self.auth.get_auth()

    def auth_user_pin(self):
        keys = self.auth.get_auth_keys()

        oauth1_user_handler = tweepy.OAuth1UserHandler(
            keys.consumer_key, keys.consumer_secret,
            callback="oob"
        )

        print(oauth1_user_handler.get_authorization_url())

        verifier = input("Input PIN: ")
        access_token, access_token_secret = oauth1_user_handler.get_access_token(
            verifier
        )

        m_keys = Auth.Keys()

        m_keys.consumer_key = keys.consumer_key
        m_keys.consumer_secret = keys.consumer_secret
        m_keys.access_token = access_token
        m_keys.access_token_secret = access_token_secret

        self.auth.set_auth_keys(m_keys)

        self.api = self.auth.get_auth()

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

    def tweets_df_auth_user(self):
        user = self.api.verify_credentials(skip_status=True)
        count = 0
        # max_count = 4000
        page_count = 0

        df = pd.DataFrame()
        rows = [df]

        for page in tweepy.Cursor(
                self.api.user_timeline,
                screen_name=user.screen_name,
                trim_user=True,
                # exclude_replies=True,
                # include_rts=False,
                count=10
        ).pages(2):
            page_count += 1
            print(f"Processing page {page_count}:")
            for tweet in page:
                count += 1
                rows.append(
                    pd.DataFrame([[tweet.id, tweet.author.id, tweet.text]], columns=['tweet_id', 'author_id', 'text']))
                print(f"Received {count} tweets.")

        df = pd.concat(rows, ignore_index=True)
        df.transpose()
        return df

    def update_auth_user_pfp(self, filename):
        user = self.api.update_profile_image(filename=filename, skip_status=True)
