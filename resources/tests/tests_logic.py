from django.test import TestCase
from .factories import ResourceFactory, TagFactory
from ..logic import search_resources


class SearchModelTestCase(TestCase):
    """This class defines the test suite for the Search logic"""

    def test_logic_search_resource(self):
        """Test if you can search a resource directly in the model"""
        # Arrange
        resources = [
            ResourceFactory(
                name='Kanban',
                url='https://en.wikipedia.org/wiki/Kannban'
            ),
            ResourceFactory(
                name='Atlassian',
                url='https://www.atlassian.com/agile/kanban'
            ),
            ResourceFactory(
                name='AGILE WEB DEVELOPMENT & OPERATIONS',
                url='http://www.agileweboperations.com/'
            ),
            ResourceFactory(
                name='Youtube',
                url='https://www.youtube.com/'
            ),
        ]
        tag = TagFactory(name='kanban')
        tag2 = TagFactory(name='scrum')
        resources[2].tags.add(tag)
        # Act
        results = search_resources('kanBan')
        # Assert
        self.assertEquals(
            results, resources[1:2], 'The Resources found are not the expected'
        )
