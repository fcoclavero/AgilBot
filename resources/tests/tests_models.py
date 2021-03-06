from django.test import TestCase
from ..models import Resource, Tag, Type, Week, Semester
from .factories import (
    ResourceFactory,
    TagFactory,
    TypeFactory,
    WeekFactory,
    SemesterFactory
)


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
            self.old_count + 1, self.new_count, 'The Resource was not created'
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
            self.old_count - 1, self.new_count, 'The Resource was not deleted'
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
            self.old_count + 1, self.new_count, 'The Tag was not created'
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
            self.old_count - 1, self.new_count, 'The Tag was not deleted'
        )

    def test_model_tag_name(self):
        """Test if the tag's name is defined properly"""
        # Act
        self.tag = TagFactory(name='thIs-is.a_tAg')
        # Assert
        self.assertEquals(
            self.tag.name, '#ThisIsATag',
            'The name of the Tag is incorrect'
        )

    def test_model_find_or_create_tag(self):
        """Test the find_or_create_tag"""
        # Arrange:
        self.old_tag = TagFactory(name='#ThisIsATag')
        self.old_count = Tag.objects.count()
        tag_names = ['#ThisIsATag', '#ThisIsAlsoATag']
        # Act
        self.new_tags = [Tag.find_or_create_tag(t) for t in tag_names]
        # Assert
        self.new_count = Tag.objects.count()
        self.assertEquals(
            self.old_count + 1, self.new_count,
            'The number of new Tags is incorrect'
        )
        self.assertEquals(
            self.old_tag.name, '#ThisIsATag',
            'The name of the Tag is incorrect'
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
            self.old_count + 1, self.new_count, 'The Type was not created'
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
            self.old_count - 1, self.new_count, 'The Type was not deleted'
        )


class WeekModelTestCase(TestCase):
    """This class defines the test suite for the Week model tests"""

    # Arrange
    def setUp(self):
        self.old_count = Week.objects.count()
        self.week = WeekFactory.build()

    def test_model_create_resource(self):
        """Test if you can create a week directly in the model"""
        # Act
        self.week.save()
        # Assert
        self.new_count = Week.objects.count()
        self.assertEquals(
            self.old_count + 1, self.new_count, 'The Week was not created'
        )

    def test_model_delete_semester(self):
        """Test if you can delete a week directly in the model"""
        # Arrange:
        self.week.save()
        self.old_count = Week.objects.count()
        # Act
        Week.objects.filter(pk=self.week.pk).delete()
        # Assert
        self.new_count = Week.objects.count()
        self.assertEquals(
            self.old_count - 1, self.new_count, 'The Week was not deleted'
        )


class SemesterModelTestCase(TestCase):
    """This class defines the test suite for the Semester model tests"""

    # Arrange
    def setUp(self):
        self.old_count = Semester.objects.count()
        self.semester = SemesterFactory.build()

    def test_model_create_resource(self):
        """Test if you can create a semester directly in the model"""
        # Act
        self.semester.save()
        # Assert
        self.new_count = Semester.objects.count()
        self.assertEquals(
            self.old_count + 1, self.new_count, 'The Semester was not created'
        )

    def test_model_delete_semester(self):
        """Test if you can delete a semester directly in the model"""
        # Arrange:
        self.semester.save()
        self.old_count = Semester.objects.count()
        # Act
        Semester.objects.filter(pk=self.semester.pk).delete()
        # Assert
        self.new_count = Semester.objects.count()
        self.assertEquals(
            self.old_count - 1, self.new_count, 'The Semester was not deleted'
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

    def test_model_associate_weeks_to_resources(self):
        """Test if you can associate weeks to resources"""
        # Arrange:
        resources = [
            ResourceFactory(),
            ResourceFactory(),
            ResourceFactory(),
        ]
        weeks = [
            WeekFactory(),
            WeekFactory(),
            WeekFactory()
        ]
        # Act:
        for resource in resources:
            for week in weeks:
                resource.weeks.add(week)
        # Assert:
        for resource in resources:
            self.assertEquals(
                list(Resource.objects.get(pk=resource.pk).weeks.all()), weeks,
                'The weeks were not associated to the resource'
            )

    def test_model_associate_weeks_to_semester(self):
        """Test if you can associate weeks to semesters"""
        # Arrange:
        semester = SemesterFactory()
        weeks = [
            WeekFactory(),
            WeekFactory(),
            WeekFactory()
        ]
        # Act:
        for week in weeks:
            week.semester = semester
            week.save()
        # Assert:
        for week in weeks:
            self.assertEquals(
                Week.objects.get(pk=week.pk).semester, semester,
                'The weeks were not associated to the semester'
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
