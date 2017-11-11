from factory import DjangoModelFactory, fuzzy, Faker
from ..models import Resource, Tag

class ResourceFactory(DjangoModelFactory):
    class Meta:
        model = Resource

    name = Faker('word')
    url = Faker('url')


class TagFactory(DjangoModelFactory):
    class Meta:
        model = Tag

    name = Faker('word')
    internal_name = Faker('word')
