from django.test import TestCase
from ..models import Resource

# Create your tests here.
class ResourceModelTestCase(TestCase):
    """This class defines the test suite for the  Resources model tests"""

    # Arrange
    def setUp(self):
        self.old_count = Resource.objects.count()
        self.resource = Resource(
            name = 'recurso',
            url = 'http://blablabla.com'
        )

    def test_model_create_resource(self):
        """Test if you can create a resource directly in the model"""
        # Act
        self.resource.save()
        # Assert
        self.new_count = Resource.objects.count()
        self.assertEquals(self.old_count+1, self.new_count)

    def test_model_delete_resource(self):
        """Test if you can delete a resource directly in the model"""
        # Assert:
        self.resource.save()
        self.old_count = Resource.objects.count()
        # Act
        Resource.objects.filter(pk=self.resource.pk).delete()
        # Assert
        self.new_count = Resource.objects.count()
        self.assertEquals(self.old_count-1, self.new_count)
