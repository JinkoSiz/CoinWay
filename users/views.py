import requests
import logging
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.db.models import Q
from django.views.decorators.cache import cache_page

from .models import Profile, TelegramUser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import TelegramUserSerializer
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


# Create your views here.

@cache_page(60 * 15)  # Cache the view for 15 minutes
def profiles(request):
    profiles, search_query = searchProfiles(request)
    custom_range, profiles = paginateProfiles(request, profiles, 6)

    context = {'profiles': profiles, 'search_query': search_query, 'custom_range': custom_range, 'html_name': 'Профиль'}
    return render(request, 'users/profiles.html', context)


@cache_page(60 * 15)  # Cache the view for 15 minutes
def userProfile(request, pk):  # ВОТ ЭТО ХУЙНЯ ВЫБЛЯДОК СЮДА СМОТРИ
    profile = Profile.objects.get(id=pk)

    context = {'profile': profile, 'html_name': 'Профиль'}

    return render(request, 'users/user-profile.html', context)


@cache_page(60 * 15)  # Cache the view for 15 minutes
@login_required(login_url='login')
def userAccount(request):
    profile = request.user.profile

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
TELEGRAM_BOT_TOKEN = '7449944814:AAGDq0lhdGiCvc07g5M5GJQ65ZSR1eBCR-4'


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
                return photo_url
    return None


@csrf_exempt
def telegram_webhook(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_data = data['message']['from']
            user_id = user_data['id']
            first_name = user_data.get('first_name', '')
            last_name = user_data.get('last_name', '') or ''  # Устанавливаем пустую строку, если last_name отсутствует
            username = user_data.get('username', '')

            logger.debug(
                f"Parsed user data: user_id={user_id}, first_name={first_name}, last_name={last_name}, username={username}")

            if user_id is None:
                logger.error("User ID is missing")
                return JsonResponse({'status': 'failed', 'error': 'User ID is missing'}, status=400)

            user, created = TelegramUser.objects.get_or_create(
                user_id=user_id,
                defaults={
                    'first_name': first_name,
                    'last_name': last_name,
                    'username': username
                }
            )

            if not created:
                user.first_name = first_name
                user.last_name = last_name
                user.username = username
                user.save()

            django_user, created = User.objects.get_or_create(username=user_id)
            profile_image_url = get_telegram_user_photo(user_id)

            if created:
                django_user.first_name = first_name
                django_user.last_name = last_name or ''  # Устанавливаем пустую строку, если last_name отсутствует
                django_user.username = user_id
                django_user.set_unusable_password()
                django_user.save()
                profile_image_url = get_telegram_user_photo(user_id)
                Profile.objects.create(user=django_user, name=username, profile_image=profile_image_url)
            else:
                profile, profile_created = Profile.objects.get_or_create(user=django_user)
                if profile_created:
                    profile.name = username
                    profile_image_url = get_telegram_user_photo(user_id)
                    profile.profile_image = profile_image_url
                    profile.save()

            login_url = f"https://coin-way-prod-git-main-jinkosizs-projects-4c8f9ac9.vercel.app/users/telegram-login/{user_id}/"

            return JsonResponse({'status': 'success', 'login_url': login_url})

        except Exception as e:
            logger.error(f"Error in telegram_webhook: {e}")
            return JsonResponse({'status': 'failed', 'error': str(e)}, status=500)
    return JsonResponse({'status': 'failed', 'error': 'Invalid request method'}, status=405)

def telegram_login(request, user_id):
    telegram_user = get_object_or_404(TelegramUser, user_id=user_id)
    django_user = get_object_or_404(User, username=telegram_user.user_id)

    login(request, django_user)
    return redirect('account')
