from django.test import TestCase
from resources.models import Resource, Tag, Type
from .logic import add_resource_from_msg


# Create your tests here.
class BotLogictestCase(TestCase):
    """This class defines the test suite for the Bot logic"""

    def test_create_link_resource(self):
        """Test if you can create a resource of type link"""
        # Arrange:
        old_resources_count = Resource.objects.count()
        old_tags_count = Tag.objects.count()
        old_types_count = Type.objects.count()
        type = 'url'
        msg = {
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
            'text': 'https://en.wikipedia.org/wiki/Kanban_(development)\
                Kanban agile methodology for task flow management \
                #kanban #agile #methodology #wikipedia',
            'entities': [
                {'offset': 0, 'length': 50, 'type': 'url'},
                {'offset': 101, 'length': 7, 'type': 'hashtag'},
                {'offset': 109, 'length': 6, 'type': 'hashtag'},
                {'offset': 116, 'length': 12, 'type': 'hashtag'},
                {'offset': 129, 'length': 10, 'type': 'hashtag'}
            ]
        }
        # Act:
        add_resource_from_msg(msg, type)

        # Assert:
        new_resources_count = Resource.objects.count()
        new_tags_count = Tag.objects.count()
        new_types_count = Type.objects.count()
        self.assertEquals(
            old_resources_count + 1, new_resources_count,
            'The resource was not created'
        )
        self.assertEquals(
            old_tags_count + 1, new_tags_count,
            'The tags were not created'
        )
        self.assertEquals(
            old_types_count + 1, new_types_count,
            'The type was not created'
        )
