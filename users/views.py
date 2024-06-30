import requests
import logging
import os
import environ
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.db.models import Q
from django.views.decorators.cache import cache_page
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile

from .models import Profile, TelegramUser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import TelegramUserSerializer
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from pathlib import Path


env = environ.Env(
    DEBUG=(bool, False)
)

BASE_DIR = Path(__file__).resolve().parent.parent

TG_KEY = env('TG_KEY')

# Create your views here.

def profiles(request):
    profiles, search_query = searchProfiles(request)
    custom_range, profiles = paginateProfiles(request, profiles, 6)

    context = {'profiles': profiles, 'search_query': search_query, 'custom_range': custom_range, 'html_name': 'Профиль'}
    return render(request, 'users/profiles.html', context)


def userProfile(request, pk):  # ВОТ ЭТО ХУЙНЯ ВЫБЛЯДОК СЮДА СМОТРИ
    profile = Profile.objects.get(id=pk)

    context = {'profile': profile, 'html_name': 'Профиль'}

    return render(request, 'users/user-profile.html', context)


@login_required(login_url='login')
def userAccount(request):
    profile = request.user.profile
    profile_image_file = get_telegram_user_photo(request.user.username.replace("tg_", ""))
    if profile_image_file:
        profile.profile_image.save(f"telegram_{request.user.username.replace('tg_', '')}.jpg", profile_image_file)
        profile.save()

    context = {'profile': profile, 'html_name': 'Профиль'}
    return render(request, 'users/account.html', context)


class TelegramUserView(APIView):
    def post(self, request, *args, **kwargs):
        user_id = request.data.get('user_id')
        user, created = TelegramUser.objects.get_or_create(user_id=user_id, defaults=request.data)
        if not created:
            serializer = TelegramUserSerializer(user, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
        else:
            serializer = TelegramUserSerializer(user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


logger = logging.getLogger(__name__)
TELEGRAM_BOT_TOKEN = f'{TG_KEY}'


def get_telegram_user_photo(user_id):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/getUserProfilePhotos"
    params = {'user_id': user_id, 'limit': 1}
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        if data['result']['total_count'] > 0:
            file_id = data['result']['photos'][0][0]['file_id']
            file_url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/getFile"
            response = requests.get(file_url, params={'file_id': file_id})
            if response.status_code == 200:
                file_path = response.json()['result']['file_path']
                photo_url = f"https://api.telegram.org/file/bot{TELEGRAM_BOT_TOKEN}/{file_path}"

                img_temp = NamedTemporaryFile(delete=True)
                img_temp.write(requests.get(photo_url).content)
                img_temp.flush()

                return File(img_temp)
    return None


@csrf_exempt
def telegram_webhook(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_data = data['message']['from']
            user_id = user_data['id']
            first_name = user_data.get('first_name', '')
            last_name = user_data.get('last_name', '') or ''
            username = user_data.get('username', '')

            logger.debug(
                f"Parsed user data: user_id={user_id}, first_name={first_name}, last_name={last_name}, username={username}")

            if user_id is None:
                logger.error("User ID is missing")
                return JsonResponse({'status': 'failed', 'error': 'User ID is missing'}, status=400)

            telegram_user, created = TelegramUser.objects.get_or_create(
                user_id=user_id,
                defaults={
                    'first_name': first_name,
                    'last_name': last_name,
                    'username': username
                }
            )

            if not created:
                telegram_user.first_name = first_name
                telegram_user.last_name = last_name
                telegram_user.username = username
                telegram_user.save()

            # Using unique identifier for the Django user
            django_user, created = User.objects.get_or_create(username=f"tg_{user_id}")
            if created:
                django_user.first_name = first_name
                django_user.last_name = last_name
                django_user.set_unusable_password()
                django_user.save()

            profile, profile_created = Profile.objects.get_or_create(user=django_user)
            profile.name = username
            profile_image_file = get_telegram_user_photo(user_id)
            if profile_image_file:
                profile.profile_image.save(f"telegram_{user_id}.jpg", profile_image_file)
            profile.save()

            login_url = f"https://coin-way-prod-git-main-jinkosizs-projects-4c8f9ac9.vercel.app/users/telegram-login/{django_user.id}/"
            return JsonResponse({'status': 'success', 'login_url': login_url})

        except Exception as e:
            logger.error(f"Error in telegram_webhook: {e}")
            return JsonResponse({'status': 'failed', 'error': str(e)}, status=500)

    return JsonResponse({'status': 'failed', 'error': 'Invalid request method'}, status=405)


def telegram_login(request, user_id):
    django_user = get_object_or_404(User, id=user_id)
    login(request, django_user)
    return redirect('account')


def userNotifications(request):
    context = {'html_name': 'Уведомления'}
    return render(request, 'users/notifications.html', context)
