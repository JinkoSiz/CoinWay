from django.contrib import admin
from .models import Profile, TelegramUser

# Register your models here.

admin.site.register(Profile)
admin.site.register(TelegramUser)
