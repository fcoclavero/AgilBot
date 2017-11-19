from datetime import datetime
from django.test import TestCase
from resources.models import Resource, Tag, Type, Semester, Week
from .logic import add_url_resource


# Create your tests here.
class BotUrlResourceLogicTestCase(TestCase):
    """Test suite for the creation of URL based Resources using the Bot"""

    def setUp(self):
        """Setup of the testcase"""
        self.type = 'url'
        self.msg = {
            'message_id': 132,
            'from': {
                'id': 376220900,
                'is_bot': False,
                'first_name': 'Sebastián',
                'last_name': 'Fehlandt',
                'username': 'Sfehlandt',
                'language_code': 'en-US',
            },
            'chat': {
                'id': 376220900,
                'first_name': 'Sebastián',
                'last_name': 'Fehlandt',
                'username': 'Sfehlandt',
                'type': 'private',
            },
            'date': 1510944484,
            'text': 'https://en.wikipedia.org/wiki/Kanban_(development) ' +
                    'Kanban agile methodology for task flow management ' +
                    '#kanban #agile #methodology #wikipedia',
            'entities': [
                {'offset': 0, 'length': 50, 'type': 'url'},
                {'offset': 101, 'length': 7, 'type': 'hashtag'},
                {'offset': 109, 'length': 6, 'type': 'hashtag'},
                {'offset': 116, 'length': 12, 'type': 'hashtag'},
                {'offset': 129, 'length': 10, 'type': 'hashtag'}
            ]
        }
        self.tags = ['#Kanban', '#Agile', '#Methodology', '#Wikipedia']
        self.name = 'Kanban'
        self.url = 'https://en.wikipedia.org/wiki/Kanban_(development)'

    def test_url_resource_type_tags(self):
        """Test if you can create a url-resource, its type and of its tags"""
        # Arrange:
        old_resources_count = Resource.objects.count()
        old_tags_count = Tag.objects.count()
        old_types_count = Type.objects.count()

        # Act:
        add_url_resource(self.msg)

        # Assert:
        new_resources_count = Resource.objects.count()
        new_tags_count = Tag.objects.count()
        new_types_count = Type.objects.count()
        self.assertEquals(
            old_resources_count + 1, new_resources_count,
            'The resource was not created'
        )
        self.assertEquals(
            old_types_count + 1, new_types_count,
            'The type was not created'
        )
        self.assertEquals(
            old_tags_count + 4, new_tags_count,
            'The tags were not created'
        )
        self.assertEquals(
            [resource.name for resource in Resource.objects.all()],
            [self.name],
            'The resource name is different than expected'
        )
        resource = Resource.objects.filter(name=self.name).first()
        self.assertEquals(
            resource.description,
            'agile methodology for task flow management',
            'The resource descrition is different than expected'
        )
        self.assertEquals(
            resource.type.name,
            self.type,
            'The type created in the database is different than expected'
        )
        self.assertEquals(
            [str(tag) for tag in Tag.objects.all()],
            self.tags,
            'The tags created in the database are different than expected'
        )
        self.assertEquals(
            [str(tag) for tag in resource.tags.all()],
            self.tags,
            'The tags associated to the resource are different than expected'
        )

    def test_url_resource_some_tags(self):
        """
        Test if you can create a url-resource, some of its tags but not
        previously created type and tags
        """
        # Arrange:
        Type.objects.create(name=self.type)
        Tag.objects.create(name=self.tags[0])
        old_resources_count = Resource.objects.count()
        old_tags_count = Tag.objects.count()
        old_types_count = Type.objects.count()

        # Act:
        add_url_resource(self.msg)

        # Assert:
        new_resources_count = Resource.objects.count()
        new_tags_count = Tag.objects.count()
        new_types_count = Type.objects.count()
        self.assertEquals(
            old_resources_count + 1, new_resources_count,
            'The resource was not created'
        )
        self.assertEquals(
            old_types_count, new_types_count,
            'The type was re-created'
        )
        self.assertEquals(
            old_tags_count + 3, new_tags_count,
            'The number of tags created if different than expected'
        )
        self.assertEquals(
            [resource.name for resource in Resource.objects.all()],
            [self.name],
            'The resource name is different than expected'
        )
        resource = Resource.objects.filter(name=self.name).first()
        self.assertEquals(
            resource.description,
            'agile methodology for task flow management',
            'The resource descrition is different than expected'
        )
        self.assertEquals(
            resource.type.name,
            self.type,
            'The type created in the database is different than expected'
        )
        self.assertEquals(
            [str(tag) for tag in Tag.objects.all()],
            self.tags,
            'The tags created in the database are different than expected'
        )
        self.assertEquals(
            [str(tag) for tag in resource.tags.all()],
            self.tags,
            'The tags associated to the resource are different than expected'
        )

    def test_url_update_resource(self):
        """Test if you can update url-resource"""
        # Arrange:
        type = Type.objects.create(name=self.type)
        tag = Tag.objects.create(name=self.tags[0])
        resource = Resource.objects.create(
            name='my_name_is',
            url=self.url,
            description='this is a terrible description',
            type=type
        )
        resource.tags.add(tag)
        old_resources_count = Resource.objects.count()
        old_tags_count = Tag.objects.count()
        old_types_count = Type.objects.count()
        self.msg['text'] = \
            'https://en.wikipedia.org/wiki/Kanban_(development) ' + \
            'Kanban agile methodology for task flow management ' + \
            '#kanban #agile #methodology #wikipedia'

        # Act:
        add_url_resource(self.msg)

        # Assert:
        new_resources_count = Resource.objects.count()
        new_tags_count = Tag.objects.count()
        new_types_count = Type.objects.count()
        self.assertEquals(
            old_resources_count, new_resources_count,
            'The resource was created'
        )
        self.assertEquals(
            old_types_count, new_types_count,
            'The type was re-created'
        )
        self.assertEquals(
            old_tags_count + 3, new_tags_count,
            'The number of tags created if different than expected'
        )
        self.assertEquals(
            [resource.name for resource in Resource.objects.all()],
            [self.name],
            'The resource name is different than expected'
        )
        resource = Resource.objects.filter(name=self.name).first()
        self.assertEquals(
            resource.description,
            'agile methodology for task flow management',
            'The resource descrition is different than expected'
        )
        self.assertEquals(
            resource.type.name,
            self.type,
            'The type created in the database is different than expected'
        )
        self.assertEquals(
            [str(tag) for tag in Tag.objects.all()],
            self.tags,
            'The tags created in the database are different than expected'
        )
        self.assertEquals(
            [str(tag) for tag in resource.tags.all()],
            self.tags,
            'The tags associated to the resource are different than expected'
        )


class ResourceWeekLogicTestCase(TestCase):
    """
    Test suite for the creation and association of Resources
    to Weeks using the Bot
    """

    def setUp(self):
        """Setup of the testcase"""
        self.type = 'url'
        self.msg = {
            'message_id': 132,
            'from': {
                'id': 376220900,
                'is_bot': False,
                'first_name': 'Sebastián',
                'last_name': 'Fehlandt',
                'username': 'Sfehlandt',
                'language_code': 'en-US',
            },
            'chat': {
                'id': 376220900,
                'first_name': 'Sebastián',
                'last_name': 'Fehlandt',
                'username': 'Sfehlandt',
                'type': 'private',
            },
            'date': 1510944484,
            'text': 'https://en.wikipedia.org/wiki/Kanban_(development) ' +
                    'Kanban agile methodology for task flow management ' +
                    '#kanban #agile #methodology #wikipedia',
            'entities': [
                {'offset': 0, 'length': 50, 'type': 'url'},
                {'offset': 101, 'length': 7, 'type': 'hashtag'},
                {'offset': 109, 'length': 6, 'type': 'hashtag'},
                {'offset': 116, 'length': 12, 'type': 'hashtag'},
                {'offset': 129, 'length': 10, 'type': 'hashtag'}
            ]
        }
        self.tags = ['#Kanban', '#Agile', '#Methodology', '#Wikipedia']
        self.name = 'Kanban'
        self.url = 'https://en.wikipedia.org/wiki/Kanban_(development)'
        self.semester = Semester.objects.create(year=2017, section=2)
        self.weeks = [
            Week.objects.create(
                name='Week', number=1, semester=self.semester,
                start_date=datetime.strptime('2017-10-27', '%Y-%m-%d').date(),
                end_date=datetime.strptime('2017-11-03', '%Y-%m-%d').date(),
            ),
            Week.objects.create(
                name='Week', number=2, semester=self.semester,
                start_date=datetime.strptime('2017-11-10', '%Y-%m-%d').date(),
                end_date=datetime.strptime('2017-11-16', '%Y-%m-%d').date(),
            ),
            Week.objects.create(
                name='Week', number=3, semester=self.semester,
                start_date=datetime.strptime('2017-11-17', '%Y-%m-%d').date(),
                end_date=datetime.strptime('2017-11-23', '%Y-%m-%d').date(),
            ),
            Week.objects.create(
                name='Week', number=4, semester=self.semester,
                start_date=datetime.strptime('2017-11-24', '%Y-%m-%d').date(),
                end_date=datetime.strptime('2017-11-30', '%Y-%m-%d').date(),
            ),
        ]

    def test_resource_date_within_week(self):
        """
        Test if a resource with date within a week is associated to that week
        """
        # Arrange:
        old_resources_count = Resource.objects.count()
        self.date = datetime.strptime('2017-11-17', '%Y-%m-%d')
        self.msg['date'] = self.date.timestamp()

        # Act:
        add_url_resource(self.msg)

        # Assert:
        new_resources_count = Resource.objects.count()
        self.assertEquals(
            old_resources_count + 1, new_resources_count,
            'The resource was not created'
        )
        resource = Resource.objects.filter(name=self.name).first()
        self.assertEquals(
            resource.publication_date,
            self.date.date(),
            'The resource publication date is different than expected'
        )
        self.assertTrue(
            self.weeks[3-1] in resource.weeks.all(),
            'The resource was not associated to the expected week expected'
        )

    def test_resource_date_closest_week_before(self):
        """
        Test if a resource with date outside every week
        is associated to the closest week before
        """
        # Arrange:
        old_resources_count = Resource.objects.count()
        self.date = datetime.strptime('2017-11-04', '%Y-%m-%d')
        self.msg['date'] = self.date.timestamp()

        # Act:
        add_url_resource(self.msg)

        # Assert:
        new_resources_count = Resource.objects.count()
        self.assertEquals(
            old_resources_count + 1, new_resources_count,
            'The resource was not created'
        )
        resource = Resource.objects.filter(name=self.name).first()
        self.assertEquals(
            resource.publication_date,
            self.date.date(),
            'The resource publication date is different than expected'
        )
        self.assertTrue(
            self.weeks[1-1] in resource.weeks.all(),
            'The resource was not associated to the expected week expected'
        )

    def test_resource_date_closest_week_after(self):
        """
        Test if a resource with date outside every week
        is associated to the closest week after
        """
        # Arrange:
        old_resources_count = Resource.objects.count()
        self.date = datetime.strptime('2017-11-08', '%Y-%m-%d')
        self.msg['date'] = self.date.timestamp()

        # Act:
        add_url_resource(self.msg)

        # Assert:
        new_resources_count = Resource.objects.count()
        self.assertEquals(
            old_resources_count + 1, new_resources_count,
            'The resource was not created'
        )
        resource = Resource.objects.filter(name=self.name).first()
        self.assertEquals(
            resource.publication_date,
            self.date.date(),
            'The resource publication date is different than expected'
        )
        self.assertTrue(
            self.weeks[2-1] in resource.weeks.all(),
            'The resource was not associated to the expected week expected'
        )

    def test_resource_update_ignore_weeks(self):
        """Test if you can update a resource and ignore updating weeks"""
        # Arrange:
        type = Type.objects.create(name=self.type)
        tag = Tag.objects.create(name=self.tags[0])
        resource = Resource.objects.create(
            name='my_name_is',
            url=self.url,
            description='this is a terrible description',
            type=type
        )
        old_weeks = list(resource.weeks.all())
        self.date = datetime.strptime('2017-11-17', '%Y-%m-%d')
        self.msg['date'] = self.date.timestamp()
        resource.tags.add(tag)
        old_resources_count = Resource.objects.count()
        old_tags_count = Tag.objects.count()
        old_types_count = Type.objects.count()
        self.msg['text'] = \
            'https://en.wikipedia.org/wiki/Kanban_(development) ' + \
            'Kanban agile methodology for task flow management ' + \
            '#kanban #agile #methodology #wikipedia'

        # Act:
        add_url_resource(self.msg)

        # Assert:
        new_resources_count = Resource.objects.count()
        new_tags_count = Tag.objects.count()
        new_types_count = Type.objects.count()
        self.assertEquals(
            old_resources_count, new_resources_count,
            'The resource was created'
        )
        self.assertEquals(
            old_types_count, new_types_count,
            'The type was re-created'
        )
        self.assertEquals(
            old_tags_count + 3, new_tags_count,
            'The number of tags created if different than expected'
        )
        self.assertEquals(
            [resource.name for resource in Resource.objects.all()],
            [self.name],
            'The resource name is different than expected'
        )
        resource = Resource.objects.filter(name=self.name).first()
        self.assertEquals(
            resource.description,
            'agile methodology for task flow management',
            'The resource descrition is different than expected'
        )
        self.assertEquals(
            resource.type.name,
            self.type,
            'The type created in the database is different than expected'
        )
        self.assertEquals(
            [str(tag) for tag in Tag.objects.all()],
            self.tags,
            'The tags created in the database are different than expected'
        )
        self.assertEquals(
            [str(tag) for tag in resource.tags.all()],
            self.tags,
            'The tags associated to the resource are different than expected'
        )
        new_weeks = list(resource.weeks.all())
        self.assertEquals(
            new_weeks, old_weeks,
            'The resource weeks were updated'
        )
