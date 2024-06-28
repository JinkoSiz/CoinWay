from django.shortcuts import render, redirect
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.decorators import login_required
from users.models import Profile
import logging

logger = logging.getLogger(__name__)


@login_required
def claim_exp(request):
    logger.info("claim_exp view called")
    if request.method == 'POST':
        logger.info("POST request received")
        profile = Profile.objects.get(user=request.user)
        now = timezone.now()

        if profile.last_claimed is None or now - profile.last_claimed >= timedelta(days=1):
            profile.exp += 10  # Добавляем 10 опыта, можно изменить это значение
            profile.last_claimed = now
            profile.save()
            message = "Вы успешно получили 10 опыта!"
            logger.info("Experience claimed successfully")
        else:
            next_claim_time = profile.last_claimed + timedelta(days=1)
            time_remaining = next_claim_time - now
            message = f"Вы сможете получить опыт через {time_remaining}."
            logger.info(f"Cannot claim experience yet, time remaining: {time_remaining}")

        return render(request, 'game/game.html', {'message': message})

    return render(request, 'game/game.html', {})


def game(request):
    context = {'html_name': 'Игра'}
    return render(request, 'game/game.html', context)
