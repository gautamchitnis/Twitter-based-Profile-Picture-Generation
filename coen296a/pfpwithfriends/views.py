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
from .models import PFP, Group, GroupMember, GroupTags, MemberTags
from django.contrib.auth.models import User

# Create your views here.


@login_required
@twitter_login_required
def index(request):
    group_pfps = None
    group = Group.objects.filter(creator=request.user).first()

    if group is None:
        creator = False
        user = User.objects.filter(username=request.user).first()
        group_member = GroupMember.objects.filter(user=user.id).first()
        if group_member is not None:
            group = group_member.group
            group_pfps = PFP.objects.filter(group=group_member.group)
    else:
        group_pfps = PFP.objects.filter(group=group)
        creator = True

    context = {
        'pfps': group_pfps if group_pfps is not None else None,
        'is_group_creator': creator,
        'group_name': group.name if group is not None or group_member is not None else None
    }

    return render(request, 'pfpwithfriends/home.html', context)


@login_required
@twitter_login_required
def gen_token(request):
    twitter_user = TwitterUser.objects.filter(user=request.user).first()

    group_member = GroupMember.objects.filter(user=twitter_user.user.id).first()

    group_members = GroupMember.objects.filter(group=group_member.group.id)

    twm = TWManager()

    tokens = []

    for member in group_members:

        '''
            Step 1: Authorize User
        '''
        twitter_user = TwitterUser.objects.filter(user=member.user.id).first()
        twm.auth_user(twitter_user)

        '''
            Step 2: Fetch Tweets of User
        '''
        df = twm.tweets_df_auth_user()

        '''
            Step 3: Clean and Tokenize Tweets
        '''
        cleaner = Cleaner()

        df = cleaner.clean_up(df)

        for idx, row in df.iterrows():
            tokens.extend(row['lemma_tokens'])

    tokens = list(set(tokens))

    tweet_topics = ", ".join(tokens)

    group_tags = GroupTags(group=group_member.group, tags=tweet_topics)

    group_tags.save()

    return redirect(show_tokens)


@login_required
@twitter_login_required
def show_tokens(request):
    group_member = GroupMember.objects.filter(user=request.user).first()

    group_tags = GroupTags.objects.filter(group=group_member.group.id).first()

    context = {
        'tags': group_tags.tags if group_tags is not None else None
    }

    return render(request, 'pfpwithfriends/show_tags.html', context)


@login_required
@twitter_login_required
def add_member_tokens(request):
    group_member = GroupMember.objects.filter(user=request.user).first()
    tags = request.POST['tags']
    # todo: format data
    member_tags = MemberTags(member=group_member, tags=tags)
    member_tags.save()

    return redirect(index)

@login_required
@twitter_login_required
def gen_pfp(request):
    group_member = GroupMember.objects.filter(user=request.user).first()

    group_members = GroupMember.objects.filter(group=group_member.group)

    tokens = []

    for member in group_members:
        member_tags = MemberTags.objects.filter(member=member).first()
        if member_tags is not None:
            split_tags = member_tags.tags.split(",")
            tokens.extend(split_tags)

    tweet_topics = ", ".join(tokens)

    '''
        Step 4: Generate Profile Picture Using Tokenized Tweets
    '''
    pm = PicMaker(url=config('GEN_URL'))

    gen_count = 0
    gen_limit = 3

    while gen_count != gen_limit:
        gen_count += 1

        data = pm.generate_image_from_prompt(tweet_topics)

        fp = BytesIO()
        fp.write(data)

        pfp = PFP(pfp=files.File(fp, f"group_{group_member.group.id}.png"), group=group_member.group)
        pfp.save()

    return redirect(index)


@login_required
@twitter_login_required
def update_pfp(request, pfp_id):
    group_member = GroupMember.objects.filter(user=request.user).first()

    group_members = GroupMember.objects.filter(group=group_member.group)

    for member in group_members:
        twitter_user = TwitterUser.objects.filter(user=member.user).first()

        twm = TWManager()
        '''
            Step 1: Authorize User
        '''
        twm.auth_user(twitter_user)

        '''
            Step 5: Update Profile Picture of the User
        '''
        user_pfp = PFP.objects.filter(id=pfp_id).first()
        twm.update_auth_user_pfp(user_pfp.pfp.path)

    return redirect(index)


@login_required
@twitter_login_required
def vote_pfp(request, pfp_id):
    pfp = PFP.objects.filter(id=pfp_id).first()
    pfp.votes += 1
    pfp.save()
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
