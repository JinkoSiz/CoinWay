from django.shortcuts import render


# Create your views here.
def game(request):
    context = {'html_name': 'Игра'}
    return render(request, 'game/game.html', context)
