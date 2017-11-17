from resources.models import Resource, Tag, Type


def add_resource_from_msg(msg, msg_type):
    msg_content = msg['text']
    msg_entities = msg['entities']
    url = None
    description = msg_content
    tags = []

    # Get url and tags:
    for entity in msg_entities:
        initial = entity['offset']
        final = entity['offset'] + entity['length']
        if entity['type'] == 'url':
            url = msg_content[initial:final]
        elif entity['type'] == 'hashtag':
            tags.append(msg_content[initial:final])

    # Get description and name
    description = msg_content.replace(url, '')
    for t in tags:
        description = description.replace(t, '')
    description = description.strip()
    [name, description] = description.split(' ', 1)

    if url is None:
        return

    # Create Type, Resource and Tags:
    type_objects = Type.objects.filter(name=msg_type)
    if type_objects.count() == 0:
        type_obj = Type.objects.create(name=msg_type)
    else:
        type_obj = type_objects.first()

    resource = Resource.objects.create(
        name=name,
        description=description,
        url=url,
        type=type_obj
    )
    for t in tags:
        tag = Tag.objects.create(name=t)
        resource.tags.add(tag)
