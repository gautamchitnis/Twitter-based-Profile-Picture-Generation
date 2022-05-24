from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('generate', views.gen_pfp, name='generate'),
    path('update_pfp/<int:pfp_id>', views.update_pfp, name='update_pfp')
]