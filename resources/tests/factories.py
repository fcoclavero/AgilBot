from factory import DjangoModelFactory, fuzzy, Faker
from ..models import Resource, Tag, Type

class ResourceFactory(DjangoModelFactory):
    class Meta:
        model = Resource

    name = Faker('word')
    url = Faker('url')


class TagFactory(DjangoModelFactory):
    class Meta:
        model = Tag

    name = Faker('sentence')


class TypeFactory(DjangoModelFactory):
    class Meta:
        model = Type

    name = Faker('file_extension')
