from datetime import datetime
from resources.models import Resource, Tag, Type, Week
STATUS_IGNORED = 0
STATUS_CREATED = 1
STATUS_UPDATED = 2


# ------------------- Auxiliary functions -----------------
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


def associate_weeks(date, resource):
    # If the resource was publicated within 1 or more weeks:
    weeks = Week.objects.filter(
        start_date__lte=date).filter(end_date__gte=date)
    if weeks:
        for week in weeks:
            resource.weeks.add(week)
        return list(weeks)

    # Otherwise:
    w_after = Week.objects.filter(start_date__gt=date).\
        order_by('start_date').first()

    w_before = Week.objects.filter(end_date__lt=date).\
        order_by('-end_date').first()

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
def add_url_resource(msg):
    if 'text' not in msg or 'entities' not in msg:
        return STATUS_IGNORED
    msg_content = msg['text']
    msg_entities = msg['entities']
    date = get_date(msg['date'])
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
    if status == STATUS_CREATED:
        weeks = associate_weeks(date, resource)
    return status, weeks
