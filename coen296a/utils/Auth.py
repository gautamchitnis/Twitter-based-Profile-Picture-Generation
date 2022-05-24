import tweepy
from decouple import config
from django.contrib.auth.models import User
from authorization.models import TwitterUser


class Auth:
    cb_url = ""

    class Keys:
        consumer_key = ""
        consumer_secret = ""
        access_token = ""
        access_token_secret = ""

    def __init__(self, cb_url=""):
        self.keys = self.Keys()
        self.cb_url = cb_url

    def get_auth(self):
        keys = self.get_auth_keys()

        auth = tweepy.OAuth1UserHandler(
            keys.consumer_key, keys.consumer_secret, keys.access_token, keys.access_token_secret
        )

        api = tweepy.API(auth)
        return api

    def set_auth_keys(self, keys=None):
        if keys is None:
            self.keys.consumer_key = config('TWITTER_CONSUMER_KEY')
            self.keys.consumer_secret = config('TWITTER_CONSUMER_SECRET')
            self.keys.access_token = config('TWITTER_ACCESS_TOKEN')
            self.keys.access_token_secret = config('TWITTER_ACCESS_TOKEN_SECRET')
        else:
            self.keys.consumer_key = keys.consumer_key
            self.keys.consumer_secret = keys.consumer_secret
            self.keys.access_token = keys.access_token
            self.keys.access_token_secret = keys.access_token_secret

    def get_auth_keys(self):
        return self.keys

    def oauth_login(self):
        oauth1_user_handler = tweepy.OAuth1UserHandler(
            self.keys.consumer_key, self.keys.consumer_secret,
            callback=self.cb_url
        )
        url = oauth1_user_handler.get_authorization_url(signin_with_twitter=True)
        request_token = oauth1_user_handler.request_token["oauth_token"]
        request_secret = oauth1_user_handler.request_token["oauth_token_secret"]
        return url, request_token, request_secret

    def handle_cb(self, oauth_token=None, oauth_token_secret=None, oauth_verifier=None):
        oauth1_user_handler = tweepy.OAuthHandler(
            self.keys.consumer_key, self.keys.consumer_secret,
            callback=self.cb_url
        )
        oauth1_user_handler.request_token = {
            'oauth_token': oauth_token,
            'oauth_token_secret': oauth_token_secret
        }
        access_token, access_token_secret = oauth1_user_handler.get_access_token(oauth_verifier)
        return access_token, access_token_secret

    def get_me(self):
        try:
            client = tweepy.Client(
                consumer_key=self.keys.consumer_key, consumer_secret=self.keys.consumer_secret,
                access_token=self.keys.access_token,
                access_token_secret=self.keys.access_token_secret
            )
            info = client.get_me(user_auth=True)
            return info
        except Exception as e:
            print(e)
            return None

    def create_update_user_from_twitter(self, twitter_user_new):
        twitter_user = TwitterUser.objects.filter(twitter_id=twitter_user_new.twitter_id).first()
        if twitter_user is None:
            user = User.objects.filter(username=twitter_user_new.screen_name).first()
            if user is None:
                user = User(username=twitter_user_new.screen_name,
                            first_name=twitter_user_new.name)
                user.save()
            twitter_user = TwitterUser(twitter_id=twitter_user_new.twitter_id,
                                       name=twitter_user_new.name,
                                       screen_name=twitter_user_new.screen_name,
                                       profile_image_url=twitter_user_new.profile_image_url)
            twitter_user.user = user
            twitter_user.twitter_oauth_token = twitter_user_new.twitter_oauth_token
            twitter_user.save()
            return user, twitter_user
        else:
            twitter_user.twitter_oauth_token = twitter_user_new.twitter_oauth_token
            twitter_user.save()
            user = twitter_user.user
            if user is not None:
                return user, twitter_user
            else:
                return None, twitter_user
