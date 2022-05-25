from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('generate', views.gen_pfp, name='generate'),
    path('update_pfp/<int:pfp_id>', views.update_pfp, name='update_pfp'),
    path('group/create', views.show_create_group, name='create_group_form'),
    path('api/group/create', views.create_group, name='create_group'),
    path('group/join', views.show_join_group, name='join_group_form'),
    path('api/group/join', views.join_group, name='join_group')
]