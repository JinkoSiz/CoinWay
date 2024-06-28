from django.shortcuts import render, redirect
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from datetime import timedelta
from django.contrib import messages
import logging
from users.models import Profile

logger = logging.getLogger(__name__)


@login_required
def claim_exp(request):
    logger.info("claim_exp view called")
    profile = Profile.objects.get(user=request.user)
    now = timezone.now()
    time_remaining = None
    next_claim_time_str = None

    if request.method == 'POST':
        logger.info("POST request received")

        if profile.last_claimed is None or now - profile.last_claimed >= timedelta(hours=12):
            profile.exp += 50  # Добавляем 50 опыта, можно изменить это значение
            profile.last_claimed = now
            profile.save()
            message = "You got 50 exp!"
            logger.info("Experience claimed successfully")
        else:
            next_claim_time = profile.last_claimed + timedelta(hours=12)
            time_remaining = next_claim_time - now
            if time_remaining.total_seconds() > 0:
                next_claim_time_str = str(time_remaining).split('.')[0]  # Убираем микросекунды
                message = f"You can get more in {next_claim_time_str}."
            else:
                message = "Вы можете получить опыт сейчас."
            logger.info(f"Cannot claim experience yet, time remaining: {next_claim_time_str}")

        return render(request, 'game/game.html',
                      {'message': message, 'exp': profile.exp, 'next_claim_time_str': next_claim_time_str})

    if profile.last_claimed:
        next_claim_time = profile.last_claimed + timedelta(hours=12)
        time_remaining = next_claim_time - now
        if time_remaining.total_seconds() > 0:
            next_claim_time_str = str(time_remaining).split('.')[0]  # Убираем микросекунды

    return render(request, 'game/game.html', {'exp': profile.exp, 'next_claim_time_str': next_claim_time_str})


def game(request):
    context = {'html_name': 'Игра', 'exp': request.user.profile.exp}
    return render(request, 'game/game.html', context)
