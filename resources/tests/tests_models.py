from django.test import TestCase
from ..models import Resource, Tag
from .factories import ResourceFactory, TagFactory

# Create your tests here.
class ResourceModelTestCase(TestCase):
    """This class defines the test suite for the Resources model tests"""

    # Arrange
    def setUp(self):
        self.old_count = Resource.objects.count()
        self.resource = ResourceFactory.build()

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


class TagModelTestCase(TestCase):
    """This class defines the test suite for the Tags model tests"""

    # Arrange
    def setUp(self):
        self.old_count = Tag.objects.count()
        self.tag = TagFactory.build()

    def test_model_create_tag(self):
        """Test if you can create a tag directly in the model"""
        # Act
        self.tag.save()
        # Assert
        self.new_count = Tag.objects.count()
        self.assertEquals(self.old_count+1, self.new_count)

    def test_model_delete_tag(self):
        """Test if you can delete a tag directly in the model"""
        # Assert:
        self.tag.save()
        self.old_count = Tag.objects.count()
        # Act
        Tag.objects.filter(pk=self.tag.pk).delete()
        # Assert
        self.new_count = Tag.objects.count()
        self.assertEquals(self.old_count-1, self.new_count)
