from django.db import models
import string


# Create your models here.
class Semester(models.Model):
    year = models.IntegerField(
        verbose_name='año'
    )
    section = models.IntegerField(
        verbose_name='año'
    )
    create_timestamp = models.DateTimeField(
        auto_now_add=True, editable=False,
        verbose_name='Fecha de creación'
    )
    update_timestamp = models.DateTimeField(
        auto_now=True, editable=False,
        verbose_name='Fecha de modificación'
    )

    class Meta:
        verbose_name = 'Semestre'
        verbose_name_plural = 'Semestres'

    def __str__(self):
        return 'Semestre ' + str(self.year) + ' - ' + str(self.section)


class Week(models.Model):
    name = models.CharField(
        max_length=50, blank=True, verbose_name='nombre'
    )
    number = models.IntegerField(
        verbose_name='numero'
    )
    create_timestamp = models.DateTimeField(
        auto_now_add=True, editable=False,
        verbose_name='Fecha de creación'
    )
    update_timestamp = models.DateTimeField(
        auto_now=True, editable=False,
        verbose_name='Fecha de modificación'
    )
    semester = models.ForeignKey(
        Semester, related_name='semester', blank=True, null=True,
        verbose_name=Semester._meta.verbose_name,
        on_delete=models.SET_NULL
    )

    class Meta:
        verbose_name = 'Semana'
        verbose_name_plural = 'Semanas'

    def __str__(self):
        return self.name + ' ' + str(self.number)


class Tag(models.Model):
    name = models.CharField(
        max_length=50, blank=True, verbose_name='nombre'
    )
    internal_name = models.CharField(
        max_length=50, blank=True, editable=False,
        verbose_name='nombre interno'
    )
    create_timestamp = models.DateTimeField(
        auto_now_add=True, editable=False,
        verbose_name='Fecha de creación'
    )
    update_timestamp = models.DateTimeField(
        auto_now=True, editable=False,
        verbose_name='Fecha de modificación'
    )

    class Meta:
        verbose_name = 'Etiqueta'
        verbose_name_plural = 'Etiquetas'

    def __str__(self):
        return self.internal_name

    def save(self, *args, **kwargs):
        int_name = str(self.name)
        int_name = int_name.replace('-', ' ')
        int_name = int_name.replace('_', ' ')
        int_name = int_name.replace('.', ' ')
        int_name = int_name.title()
        int_name = int_name.replace(' ', '')
        self.internal_name = int_name
        super(Tag, self).save(*args, **kwargs)


class Type(models.Model):
    name = models.CharField(
        max_length=50, blank=True, verbose_name='nombre'
    )
    create_timestamp = models.DateTimeField(
        auto_now_add=True, editable=False,
        verbose_name='Fecha de creación'
    )
    update_timestamp = models.DateTimeField(
        auto_now=True, editable=False,
        verbose_name='Fecha de modificación'
    )

    class Meta:
        verbose_name = 'Tipo'
        verbose_name_plural = 'Tipos'

    def __str__(self):
        return self.name


class Resource(models.Model):
    name = models.CharField(
        max_length=50, blank=True, verbose_name='nombre'
    )
    url = models.URLField(blank=False)
    create_timestamp = models.DateTimeField(
        auto_now_add=True, editable=False,
        verbose_name='Fecha de creación'
    )
    update_timestamp = models.DateTimeField(
        auto_now=True, editable=False,
        verbose_name='Fecha de modificación'
    )
    tags = models.ManyToManyField(
        Tag, related_name='resources', blank=True,
        verbose_name=Tag._meta.verbose_name_plural
    )
    type = models.ForeignKey(
        Type, related_name='type', blank=True, null=True,
        verbose_name=Type._meta.verbose_name,
        on_delete=models.SET_NULL
    )
    weeks = models.ManyToManyField(
        Week, related_name='weeks', blank=True,
        verbose_name=Week._meta.verbose_name_plural
    )

    class Meta:
        verbose_name = 'Recurso'
        verbose_name_plural = 'Recursos'

    def __str__(self):
        return self.name + ': ' + self.url
