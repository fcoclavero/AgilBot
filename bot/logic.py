import pprint
import telepot

from datetime import datetime
from telepot.loop import MessageLoop

from bot.constants import *
from bot.models import Bot
from resources.models import Resource, Tag, Type, Week, Semester


class SingletonTelegramBot:
	singleton_bot = None

	def __init__(self):

		def handle(msg):
			content_type, chat_type, chat_id = telepot.glance(msg)

			print('**************************************')
			print(content_type, chat_type, chat_id)
			pp = pprint.PrettyPrinter(indent=4)
			pp.pprint(msg)

			if content_type == 'text':
				# Get commands - must be the first entity of msg for now
				entity = msg['entities'][0]
				if entity['type'] == "bot_command":
					command = msg['text'][entity['offset']:entity['length']]
					if command == "/help":
						bot.sendMessage(
							chat_id,
							HELP_RESPONSE
						)

				if 'chat_id' in msg['text']:
					send_chat_id(chat_id)
				else:
					content_type = 'link'  # TODO: cambiar hardcodeado D:
					create_url_resource(content_type, chat_type, chat_id, msg)

		def send_chat_id(chat_id):
			response = 'El id de este chat es el siguiente: ' + str(chat_id)
			bot.sendMessage(chat_id, response)

		def create_url_resource(content_type, chat_type, chat_id, msg):
			[status, weeks] = add_url_resource(msg, chat_id)
			if status == STATUS_CREATED:
				response = 'El recurso fue creado con exito'
				if weeks and weeks != []:
					response = response + \
							   ' y asociado a las semanas: ' + str(weeks)
				bot.sendMessage(chat_id, response)
			elif status == STATUS_UPDATED:
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


def get_date(date):
	return datetime.fromtimestamp(date).date()


def create_type(msg_type):
	type_objects = Type.objects.filter(name=msg_type)
	if type_objects.count() == 0:
		return Type.objects.create(name=msg_type)
	else:
		return type_objects.first()


def create_tags_and_associate_to_resource(tags, resource):
	for t in tags:
		tag = Tag.find_or_create_tag(t)
		resource.tags.add(tag)


def associate_weeks(date, resource, chat_id):
	# If the resource was publicated within 1 or more weeks:
	semester = Semester.objects.filter(chat_id=chat_id).first()
	weeks = Week.objects.filter(semester=semester). \
		filter(start_date__lte=date).filter(end_date__gte=date)
	if weeks:
		for week in weeks:
			resource.weeks.add(week)
		return list(weeks)

	# Otherwise:
	w_after = Week.objects.filter(semester=semester). \
		filter(start_date__gt=date).order_by('start_date').first()

	w_before = Week.objects.filter(semester=semester). \
		filter(end_date__lt=date).order_by('-end_date').first()

	if not w_before and w_after:
		week = w_after
	elif w_before and not w_after:
		week = w_before
	elif not w_before and not w_after:
		return False
	elif w_after.start_date - date > date - w_before.end_date:
		week = w_before
	else:
		week = w_after

	resource.weeks.add(week)
	return [week]


# ------------------- Main functions -----------------
def add_url_resource(msg, chat_id):
	if 'text' not in msg or 'entities' not in msg:
		return STATUS_IGNORED, None
	msg_content = msg['text']
	msg_entities = msg['entities']
	date = get_date(msg['date'])
	msg_type = 'url'
	url = None
	description = msg_content
	tags = []
	mentions = []

	# Get url and tags:
	for entity in msg_entities:
		initial = entity['offset']
		final = entity['offset'] + entity['length']
		if entity['type'] == 'url':
			url = msg_content[initial:final]
		elif entity['type'] == 'hashtag':
			tags.append(msg_content[initial:final])
		elif entity['type'] == 'mention':
			mentions.append(msg_content[initial:final])

	if url is None:
		return STATUS_IGNORED, None

	# Get description and name
	description = msg_content.replace(url, '')
	for t in tags:
		description = description.replace(t, '')
	for m in mentions:
		description = description.replace(m, '')

	description = description.strip()

	name = "Nuevo recurso"	

	# Create Type, Resource and Tags:
	type_obj = create_type(msg_type)

	resource_search = Resource.objects.filter(url=url)
	if resource_search.count() == 0:
		resource = Resource.objects.create(
			name=name,
			description=description,
			url=url,
			type=type_obj,
			publication_date=date
		)
		status = STATUS_CREATED
	else:
		resource = resource_search.first()
		resource.name = name
		resource.description = description
		resource.save()
		status = STATUS_UPDATED

	create_tags_and_associate_to_resource(tags, resource)
	weeks = []
	# if status == STATUS_CREATED:
	weeks = associate_weeks(date, resource, chat_id)
	return status, weeks
