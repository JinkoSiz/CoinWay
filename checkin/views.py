from django.shortcuts import render


# Create your views here.
def checkin(request):
    context = {'html_name': 'Игра'}
    return render(request, 'checkin/checkin.html', context)
