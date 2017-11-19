from factory import DjangoModelFactory, Faker
from ..models import Resource, Tag, Type, Week, Semester


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


class WeekFactory(DjangoModelFactory):
    class Meta:
        model = Week

    name = Faker('word')
    number = Faker('pyint')
    start_date = Faker('date')
    end_date = Faker('date')


class SemesterFactory(DjangoModelFactory):
    class Meta:
        model = Semester

    year = Faker('year')
    section = Faker('pyint')
