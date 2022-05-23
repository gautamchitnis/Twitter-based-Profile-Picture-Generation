import tweepy


class Auth:

    class Keys:
        consumer_key = ""
        consumer_secret = ""
        access_token = ""
        access_token_secret = ""

    def __init__(self):
        self.keys = self.Keys()

    def get_auth(self):
        keys = self.get_auth_keys()

        auth = tweepy.OAuth1UserHandler(
            keys.consumer_key, keys.consumer_secret, keys.access_token, keys.access_token_secret
        )

        api = tweepy.API(auth)
        return api

    def set_auth_keys(self, keys=None):
        if keys is None:
            # TODO: Set Key values here
            # TODO: Use env or a file to populate keys

            self.keys.consumer_key = ""
            self.keys.consumer_secret = ""
            self.keys.access_token = ""
            self.keys.access_token_secret = ""
        else:
            self.keys.consumer_key = keys.consumer_key
            self.keys.consumer_secret = keys.consumer_secret
            self.keys.access_token = keys.access_token
            self.keys.access_token_secret = keys.access_token_secret

    def get_auth_keys(self):
        return self.keys
