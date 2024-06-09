from django.urls import path
from . import views

urlpatterns = [
    path('telegram-webhook/', views.telegram_webhook, name='telegram_webhook'),
    path('telegram-login/<str:user_id>/', views.telegram_login, name='telegram_login'),

    path('', views.profiles, name='profiles'),
    path('profile/<str:pk>/', views.userProfile, name='user-profile'),
    path('account/', views.userAccount, name='account'),
]
