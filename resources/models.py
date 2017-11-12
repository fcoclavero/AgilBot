from django.db import models
import string


# Create your models here.
class Tag(models.Model):

    name = models.CharField(max_length=50, blank=True, verbose_name='nombre')
    internal_name = models.CharField(
        max_length=50, blank=True, editable=False,
        verbose_name='nombre interno'
    )
    create_timestamp = models.DateTimeField(
        auto_now_add=True, editable=False, verbose_name='Fecha de creación'
    )
    update_timestamp = models.DateTimeField(
        auto_now=True, editable=False, verbose_name='Fecha de modificación'
    )

    class Meta:
        verbose_name = 'Etiqueta'
        verbose_name_plural = 'Etiquetas'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        int_name = str(self.name)
        int_name = int_name.replace('-', ' ')
        int_name = int_name.replace('_', ' ')
        int_name = int_name.replace('.', ' ')
        int_name = int_name.title()
        int_name = int_name.replace(' ', '')
        self.internal_name = int_name
        super(Tag, self).save(*args, **kwargs)


class Resource(models.Model):

    name = models.CharField(max_length=50, blank=True, verbose_name='nombre')
    url = models.URLField(blank=False)
    create_timestamp = models.DateTimeField(
        auto_now_add=True, editable=False, verbose_name='Fecha de creación'
    )
    update_timestamp = models.DateTimeField(
        auto_now=True, editable=False, verbose_name='Fecha de modificación'
    )
    tags = models.ManyToManyField(
        Tag, related_name='resources', blank=True,
        verbose_name = Tag._meta.verbose_name_plural
    )

    class Meta:
        verbose_name = 'Recurso'
        verbose_name_plural = 'Recursos'

    def __str__(self):
        return self.name + ': ' + self.url
