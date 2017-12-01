from itertools import chain
from .models import Resource, Tag
# Create intermediary functions here


def search_resources(keyword):
    """
    Search Resources by keywords, considering, their names, urls
    and associated Tags
    """
    keyword = Tag.transform_name(keyword)
    if keyword[0] == '#':
        keyword = keyword[1:]
    resource_name_queryset = Resource.objects.filter(name__contains=keyword)
    resource_description_queryset = Resource.objects.filter(
        description__contains=keyword
    )
    resource_url_queryset = Resource.objects.filter(url__contains=keyword)
    tag_queryset = Tag.objects.filter(name__contains=keyword)
    resource_tag_queryset = Resource.objects.filter(tags__in=tag_queryset)
    result_list = list(chain(
        resource_name_queryset,
        resource_description_queryset,
        resource_url_queryset,
        resource_tag_queryset
    ))
    return result_list
