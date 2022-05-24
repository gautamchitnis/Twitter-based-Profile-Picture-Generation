from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('generate', views.gen_pfp, name='generate'),
]