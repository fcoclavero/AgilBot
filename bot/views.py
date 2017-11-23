from django.http import HttpResponse
import pprint
from bot import logic
from bot.models import Bot


class SingletonTelegramBot:
    singleton_bot = None

    def __init__(self):
        import telepot
        from telepot.loop import MessageLoop

        def handle(msg):
            content_type, chat_type, chat_id = telepot.glance(msg)

            print('**************************************')
            print(content_type, chat_type, chat_id)
            pp = pprint.PrettyPrinter(indent=4)
            pp.pprint(msg)

            if content_type == 'text':
                if 'chat_id' in msg['text']:
                    send_chat_id(chat_id)
                else:
                    content_type = 'url'
                    create_url_resource(content_type, chat_type, chat_id, msg)

        def send_chat_id(chat_id):
            response = 'El id de este chat es el siguiente: ' + str(chat_id)
            bot.sendMessage(chat_id, response)

        def create_url_resource(content_type, chat_type, chat_id, msg):
            [status, weeks] = logic.add_url_resource(msg, chat_id)
            if status == logic.STATUS_CREATED:
                response = 'El recurso fue creado con exito'
                if weeks and weeks != []:
                    response = response + \
                        ' y asociado a las semanas: ' + str(weeks)
                bot.sendMessage(chat_id, response)
            elif status == logic.STATUS_UPDATED:
                bot.sendMessage(
                    chat_id, 'El recurso fue modificado con exito'
                )

        TOKEN = Bot.get_token()

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
