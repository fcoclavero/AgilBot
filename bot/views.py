from django.http import HttpResponse
import pprint
from bot.logic import add_url_resource


class SingletonTelegramBot:
    singleton_bot = None

    def __init__(self):
        import telepot
        from telepot.loop import MessageLoop

        def handle(msg):
            print('**************************************')
            content_type, chat_type, chat_id = telepot.glance(msg)

            print(content_type, chat_type, chat_id)
            pp = pprint.PrettyPrinter(indent=4)
            pp.pprint(msg)

            if content_type == 'text':
                content_type = 'url'
                add_url_resource(msg)
                bot.sendMessage(chat_id, msg['text'])

        TOKEN = '476757125:AAF7DQDtyeClA2wPhnqedeYa5d2USWRYJyA'

        bot = telepot.Bot(TOKEN)
        bot.setWebhook()
        MessageLoop(bot, handle).run_as_thread()
        print('Listening ...')

    @classmethod
    def init_bot(self):
        if not self.singleton_bot:
            self.singleton_bot = SingletonTelegramBot()
        return self.singleton_bot


# Create your views here.
def index(request):
    SingletonTelegramBot.init_bot()
    return HttpResponse("Bot inicializado...")
