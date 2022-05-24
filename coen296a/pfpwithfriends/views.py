from django.shortcuts import render
from authorization.decorators import twitter_login_required
from django.contrib.auth.decorators import login_required
from decouple import config
from utils.Auth import Auth
from utils.TWManager import TWManager
from utils.Cleaner import Cleaner
from utils.PfpManager import PicMaker
from authorization.models import TwitterUser

# Create your views here.


@login_required
@twitter_login_required
def index(request):
    return render(request, 'pfpwithfriends/home.html')

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

    pm.generate_image_from_df(df)

    '''
        Step 5: Update Profile Picture of the User
    '''
    # twm.update_auth_user_pfp("response.png")

    return render(request, 'pfpwithfriends/home.html')
