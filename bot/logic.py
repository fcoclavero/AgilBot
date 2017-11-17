from django.core.exceptions import ValidationError
from django.core.validators import URLValidator

from resources import models


def add_resource_link(msg_text):
	split = msg_text.splt(" ")

	tags = []
	link = None
	description = []

	val = URLValidator(verify_exists=True)

	# Retrieve fields
	for txt in split:
		if link is None:
			try:
				val(txt)
				link = txt
			except ValidationError as e:
				pass

		if txt[0] == "#":
			tags.append(txt)
		else:
			description.append(txt)

	if link is not None:
		resource = Resource.objects.create(
			name=description[0],
			description=" ".join(description),
			url=link
		)
		for t in tags:
			tag = Tag.objects.create(name=t)
			resource.tags.add(tag)
		return True

