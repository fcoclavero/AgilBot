from django.shortcuts import render
from django.http import HttpResponse

from bot.logic import add_resource_link


class SingletonTelegramBot:
	singleton_bot = None

	def __init__(self):
		import sys
		import time
		import telepot
		from telepot.loop import MessageLoop

		def handle(msg):
			content_type, chat_type, chat_id = telepot.glance(msg)

			print(content_type, chat_type, chat_id)
			print(msg)

			if content_type == 'text':
				add_resource_link(msg['text'])
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