from factory import DjangoModelFactory, fuzzy, Faker
from ..models import Resource

class ResourceFactory(DjangoModelFactory):
    class Meta:
        model = Resource

    name = Faker('word')
    url = Faker('url')
