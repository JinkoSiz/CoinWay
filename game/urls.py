from django.urls import path
from . import views


urlpatterns = [
    #path('', views.game, name='game'),
    path('', views.claim_exp, name='claim_exp'),
]
