from .models import Resource, Tag
# Create intermediary functions here


def search_resources(keyword):
    """
    Search Resources by keywords, considering, their names, urls
    and associated Tags
    """
    keyword = Tag.transform_name(keyword)
    resource_name_queryset = Resource.objects.filter(name__contains=keyword)
    resource_url_queryset = Resource.objects.filter(url__contains=keyword)
    tag_queryset = Tag.objects.filter(name__contains=keyword)
    
    print(resource_name_queryset)
    print(resource_url_queryset)
    print(tag_queryset)
