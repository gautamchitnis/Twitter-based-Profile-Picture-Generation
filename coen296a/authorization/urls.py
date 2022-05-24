from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.twitter_login, name='twitter_login'),
    path('cb/', views.twitter_callback, name='twitter_callback'),
    path('logout/', views.twitter_logout, name='twitter_logout'),
]