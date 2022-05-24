from io import BytesIO

from django.core import files
from django.shortcuts import render, redirect
from authorization.decorators import twitter_login_required
from django.contrib.auth.decorators import login_required
from decouple import config
from utils.Auth import Auth
from utils.TWManager import TWManager
from utils.Cleaner import Cleaner
from utils.PfpManager import PicMaker
from authorization.models import TwitterUser
from .models import PFP

# Create your views here.


@login_required
@twitter_login_required
def index(request):
    user_pfps = PFP.objects.filter(user=request.user)
    context = {
        'pfps': user_pfps
    }
    return render(request, 'pfpwithfriends/home.html', context)


@login_required
@twitter_login_required
def gen_pfp(request):
    twitter_user = TwitterUser.objects.filter(user=request.user).first()

    auth = Auth()
    auth.set_auth_keys()
    keys = auth.get_auth_keys()
    keys.access_token = twitter_user.twitter_oauth_token.oauth_token
    keys.access_token_secret = twitter_user.twitter_oauth_token.oauth_token_secret
    auth.set_auth_keys(keys=keys)

    twm = TWManager()

    '''
        Step 1: Authorize User
    '''
    twm.api = auth.get_auth()
    '''
        Step 2: Fetch Tweets of User
    '''
    df = twm.tweets_df_auth_user()

    '''
        Step 3: Clean and Tokenize Tweets
    '''
    cleaner = Cleaner()

    df = cleaner.clean_up(df)

    '''
        Step 4: Generate Profile Picture Using Tokenized Tweets
    '''
    pm = PicMaker(url=config('GEN_URL'))

    data = pm.generate_image_from_df(df)

    fp = BytesIO()
    fp.write(data)

    pfp = PFP(pfp=files.File(fp, f"user_{request.user.id}.png"), user=request.user)
    pfp.save()

    return redirect(index)


@login_required
@twitter_login_required
def update_pfp(request, pfp_id):
    twitter_user = TwitterUser.objects.filter(user=request.user).first()

    auth = Auth()
    auth.set_auth_keys()
    keys = auth.get_auth_keys()
    keys.access_token = twitter_user.twitter_oauth_token.oauth_token
    keys.access_token_secret = twitter_user.twitter_oauth_token.oauth_token_secret
    auth.set_auth_keys(keys=keys)

    twm = TWManager()
    '''
        Step 1: Authorize User
    '''
    twm.api = auth.get_auth()

    '''
        Step 5: Update Profile Picture of the User
    '''
    user_pfp = PFP.objects.filter(user=request.user, id=pfp_id).first()
    twm.update_auth_user_pfp(user_pfp.pfp.path)

    return redirect(index)
