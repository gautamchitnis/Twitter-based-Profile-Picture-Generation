from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),

    path('groups/tags', views.show_tokens, name='show_tags'),
    path('member/tags/add', views.add_member_tokens, name='add_member_tags'),
    path('generate/pfp', views.gen_pfp, name='generate_pfp'),
    path('generate/tags', views.gen_token, name='generate_tags'),
    path('update_pfp/<int:pfp_id>', views.update_pfp, name='update_pfp'),
    path('vote_pfp/<int:pfp_id>', views.vote_pfp, name='vote_pfp'),

    path('group/create', views.show_create_group, name='create_group_form'),
    path('api/group/create', views.create_group, name='create_group'),

    path('group/join', views.show_join_group, name='join_group_form'),
    path('api/group/join', views.join_group, name='join_group')
]