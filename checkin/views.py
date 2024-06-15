from django.shortcuts import render, get_object_or_404
from django.views.decorators.cache import cache_page


# Create your views here.
def checkin(request):
    context = {'html_name': 'Игра с писюном'}
    return render(request, 'checkin/checkin.html')
