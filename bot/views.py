from django.http import HttpResponse
from bot.logic import SingletonTelegramBot


# Create your views here.
def index(request):
    SingletonTelegramBot.init_bot()
    return HttpResponse("Bot inicializado...")
