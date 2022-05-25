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
from .models import PFP, Group, GroupMember
from django.contrib.auth.models import User

# Create your views here.


@login_required
@twitter_login_required
def index(request):
    user_pfps = PFP.objects.filter(user=request.user)

    group = Group.objects.filter(creator=request.user).first()

    if group is None:
        creator = False
        user = User.objects.filter(username=request.user).first()
        group_member = GroupMember.objects.filter(user=user.id).first()
        group = group_member.group
    else:
        creator = True

    context = {
        'pfps': user_pfps,
        'is_group_creator': creator,
        'group_name': group.name if group is not None or group_member is not None else None
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


@login_required
@twitter_login_required
def show_create_group(request):
    return render(request, 'pfpwithfriends/create_group.html')


@login_required
@twitter_login_required
def create_group(request):
    name = request.POST['name']
    group = Group(name=name, creator=request.user)
    group.save()
    group_member = GroupMember(user=request.user, group=group)
    group_member.save()

    return redirect(index)


@login_required
@twitter_login_required
def show_join_group(request):
    return render(request, 'pfpwithfriends/join_group.html')


@login_required
@twitter_login_required
def join_group(request):
    name = request.POST['name']
    group = Group.objects.filter(name=name).first()
    group_member = GroupMember(user=request.user, group=group)
    group_member.save()

    return redirect(index)
