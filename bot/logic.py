import pprint
import telepot

from datetime import datetime
from telepot.loop import MessageLoop

from bot.constants import *
from bot.models import Bot
from resources.models import Resource, Semester, Tag, Type, Week


class SingletonTelegramBot:
	singleton_bot = None

	@classmethod
	def init_bot(cls):
		if not cls.singleton_bot:
			cls.singleton_bot = SingletonTelegramBot()
		return cls.singleton_bot

	def __init__(self):
		TOKEN = Bot.get_token()
		self.bot = telepot.Bot(TOKEN)
		self.bot.setWebhook()
		MessageLoop(self.bot, self.handle_msg).run_as_thread()
		print('Listening ...')

	def handle_msg(self, msg):
		content_type, chat_type, chat_id = telepot.glance(msg)

		print('**************************************')
		print(content_type, chat_type, chat_id)
		pp = pprint.PrettyPrinter(indent=4)
		pp.pprint(msg)

		if 'text' not in msg or 'entities' not in msg:
			return STATUS_IGNORED, None

		url, description, tags, mentions, commands = parse_msg(msg)

		if content_type == 'text':
			# Handle bot commands
			for command in commands:
				if command == HELP_COMMAND:
					self.bot.sendMessage(
						chat_id,
						HELP_RESPONSE
					)
			# Manage links
			if 'chat_id' in msg['text']:
				self.send_chat_id(chat_id)
			elif url is not None:
				content_type = 'link'
				self.create_url_resource(content_type, chat_type, chat_id, msg)


	def send_chat_id(self, chat_id):
		response = ID_RESPONSE + str(chat_id)
		self.bot.sendMessage(chat_id, response)

	def create_url_resource(self, content_type, chat_type, chat_id, msg):
		[status, weeks] = add_url_resource(msg, chat_id)
		if status == STATUS_CREATED:
			response = CREATION_RESPONSE
			if weeks and weeks != []:
				response = response + \
						   ' y asociado a las semanas: ' + str(weeks)
			self.bot.sendMessage(chat_id, response)
		elif status == STATUS_UPDATED:
			self.bot.sendMessage(
				chat_id, MODIFICATION_RESPONSE
			)


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
	# If the resource was published within 1 or more weeks:
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


def parse_msg(msg):
	url = None
	tags = []
	mentions = []
	commands = []

	msg_content = msg['text']
	msg_entities = msg['entities']

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
		elif entity['type'] == 'bot_command':
			commands.append(msg_content[initial:final])

	# Get description: all text not belonging to an entity
	description = msg_content
	if url is not None:
		description = msg_content.replace(url, '')
	for t in tags:
		description = description.replace(t, '')
	for m in mentions:
		description = description.replace(m, '')
	for c in commands:
		description = description.replace(c, '')

	description = description.strip()

	return url, description, tags, mentions, commands


def add_url_resource(msg, chat_id):
	date = get_date(msg['date'])
	msg_type = 'url'

	url, description, tags, mentions, commands = parse_msg(msg)

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
	weeks = associate_weeks(date, resource, chat_id)

	return status, weeks
