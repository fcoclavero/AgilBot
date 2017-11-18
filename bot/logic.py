from resources.models import Resource, Tag, Type
STATUS_IGNORED = 0
STATUS_CREATED = 1
STATUS_UPDATED = 2

def add_url_resource(msg):
    if 'text' not in msg or 'entities' not in msg:
        return STATUS_IGNORED
    msg_content = msg['text']
    msg_entities = msg['entities']
    msg_type = 'url'
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

    if url is None:
        return STATUS_IGNORED

    # Get description and name
    description = msg_content.replace(url, '')
    for t in tags:
        description = description.replace(t, '')

    description = description.strip()
    if description.count(' ') != 0:
        [name, description] = description.split(' ', 1)
    else:
        name = description

    # Create Type, Resource and Tags:
    type_objects = Type.objects.filter(name=msg_type)
    if type_objects.count() == 0:
        type_obj = Type.objects.create(name=msg_type)
    else:
        type_obj = type_objects.first()

    resource_search = Resource.objects.filter(url=url)
    if resource_search.count() == 0:
        resource = Resource.objects.create(
            name=name,
            description=description,
            url=url,
            type=type_obj
        )
        status = STATUS_CREATED
    else:
        resource = resource_search.first()
        resource.name = name
        resource.description = description
        resource.save()
        status = STATUS_UPDATED

    for t in tags:
        tag = Tag.find_or_create_tag(t)
        resource.tags.add(tag)

    return status
