from django.shortcuts import render

# Create your views here.
def ema_authenticate(request):
    return render(request, 'telegram_bot/start.html')
