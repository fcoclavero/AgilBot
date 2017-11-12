from django.test import TestCase
from ..models import Resource, Tag, Type
from .factories import ResourceFactory, TagFactory, TypeFactory

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
        self.assertEquals(
            self.old_count+1, self.new_count, 'The Resource was not created'
        )

    def test_model_delete_resource(self):
        """Test if you can delete a resource directly in the model"""
        # Arrange:
        self.resource.save()
        self.old_count = Resource.objects.count()
        # Act
        Resource.objects.filter(pk=self.resource.pk).delete()
        # Assert
        self.new_count = Resource.objects.count()
        self.assertEquals(
            self.old_count-1, self.new_count,'The Resource was not deleted'
        )


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
        self.assertEquals(
            self.old_count+1, self.new_count, 'The Tag was not created'
        )

    def test_model_delete_tag(self):
        """Test if you can delete a tag directly in the model"""
        # Arrange:
        self.tag.save()
        self.old_count = Tag.objects.count()
        # Act
        Tag.objects.filter(pk=self.tag.pk).delete()
        # Assert
        self.new_count = Tag.objects.count()
        self.assertEquals(
            self.old_count-1, self.new_count, 'The Tag was not deleted'
        )

    def test_model_tag_internal_name(self):
        """Test if the tag's internal_name is defined properly"""
        # Act
        self.tag = TagFactory(name = 'thIs-is.a_tAg')
        # Assert
        self.assertEquals(
            self.tag.internal_name, 'ThisIsATag',
            'The internal_name of the Tag is incorrect'
        )

class TypeModelTestCase(TestCase):
    """This class defines the test suite for the Types model tests"""

    # Arrange
    def setUp(self):
        self.old_count = Type.objects.count()
        self.type = TypeFactory.build()

    def test_model_create_type(self):
        """Test if you can create a type directly in the model"""
        # Act
        self.type.save()
        # Assert
        self.new_count = Type.objects.count()
        self.assertEquals(
            self.old_count+1, self.new_count, 'The Type was not created'
        )

    def test_model_delete_type(self):
        """Test if you can delete a type directly in the model"""
        # Arrange:
        self.type.save()
        self.old_count = Type.objects.count()
        # Act
        Type.objects.filter(pk=self.type.pk).delete()
        # Assert
        self.new_count = Type.objects.count()
        self.assertEquals(
            self.old_count-1, self.new_count,'The Type was not deleted'
        )

class AssociationModelTestCase(TestCase):
    """This class defines the test suite for the association between models"""

    def test_model_associate_tags_to_resources(self):
        """Test if you can associate tags to resources"""
        # Arrange:
        resources = [
            ResourceFactory(),
            ResourceFactory(),
            ResourceFactory(),
        ]
        tags = [
            TagFactory(),
            TagFactory(),
            TagFactory()
        ]
        # Act:
        for resource in resources:
            for tag in tags:
                resource.tags.add(tag)
        # Assert:
        for resource in resources:
            self.assertEquals(
                list(Resource.objects.get(pk=resource.pk).tags.all()), tags,
                'The tags were not associated to the resource'
            )

    def test_model_associate_types_to_resources(self):
        """Test if you can associate a type to many resources"""
        # Arrange:
        resources = [
            ResourceFactory(),
            ResourceFactory(),
            ResourceFactory(),
        ]
        type = TypeFactory()
        # Act:
        for resource in resources:
            resource.type = type
            resource.save()
        # Assert:
        for resource in resources:
            self.assertEquals(
                Resource.objects.get(pk=resource.pk).type, type,
                'The type is not associated to the resource'
            )

    def test_model_remove_type_but_not_its_resource(self):
        """Test if you can delete a type and keep its resource"""
        # Arrange:
        resource = ResourceFactory()
        type = TypeFactory()
        resource.type = type
        resource.save()
        old_resource_count = Resource.objects.count()
        # Act:
        Type.objects.filter(pk=type.pk).delete()
        new_resource_count = Resource.objects.count()
        # Assert:
        self.assertEquals(
            old_resource_count,
            new_resource_count,
            'The resource was deleted'
        )
