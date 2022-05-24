from functools import wraps
from django.contrib.auth import logout
from django.http import HttpResponseRedirect
from django.urls import reverse
from utils.Auth import Auth
from .models import TwitterUser


def twitter_login_required(function):
    @wraps(function)
    def wrap(request, *args, **kwargs):
        twitter_user = TwitterUser.objects.filter(user=request.user).first()

        auth = Auth()
        auth.set_auth_keys()
        keys = auth.get_auth_keys()
        keys.access_token = twitter_user.twitter_oauth_token.oauth_token
        keys.access_token_secret = twitter_user.twitter_oauth_token.oauth_token_secret
        info = auth.get_me()

        if info is None:
            logout(request)
            return HttpResponseRedirect(reverse('twitter_login'))
        else:
            return function(request, *args, **kwargs)
    return wrap