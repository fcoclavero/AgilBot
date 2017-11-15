from django.db import models


# Create your models here.
class BaseModel(models.Model):
    create_timestamp = models.DateTimeField(
        auto_now_add=True, editable=False,
        verbose_name='Fecha de creación'
    )
    update_timestamp = models.DateTimeField(
        auto_now=True, editable=False,
        verbose_name='Fecha de modificación'
    )

    class Meta:
        abstract = True


class Semester(BaseModel):
    year = models.IntegerField(
        verbose_name='año'
    )
    section = models.IntegerField(
        verbose_name='año'
    )

    class Meta:
        verbose_name = 'Semestre'
        verbose_name_plural = 'Semestres'

    def __str__(self):
        return 'Semestre ' + str(self.year) + ' - ' + str(self.section)


class Week(BaseModel):
    name = models.CharField(
        max_length=50, blank=True, verbose_name='nombre'
    )
    number = models.IntegerField(
        verbose_name='numero'
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


class Tag(BaseModel):
    name = models.CharField(
        max_length=50, blank=True, verbose_name='nombre'
    )
    internal_name = models.CharField(
        max_length=50, blank=True, editable=False,
        verbose_name='nombre interno'
    )

    class Meta:
        verbose_name = 'Etiqueta'
        verbose_name_plural = 'Etiquetas'

    def __str__(self):
        return self.internal_name

    @staticmethod
    def transform_name(name):
        transformed_name = name
        transformed_name = transformed_name.replace('-', ' ')
        transformed_name = transformed_name.replace('_', ' ')
        transformed_name = transformed_name.replace('.', ' ')
        transformed_name = transformed_name.title()
        transformed_name = transformed_name.replace(' ', '')
        return transformed_name

    def save(self, *args, **kwargs):
        self.internal_name = Tag.transform_name(str(self.name))
        super(Tag, self).save(*args, **kwargs)


class Type(BaseModel):
    name = models.CharField(
        max_length=50, blank=True, verbose_name='nombre'
    )

    class Meta:
        verbose_name = 'Tipo'
        verbose_name_plural = 'Tipos'

    def __str__(self):
        return self.name


def image_filename(self, filename):
    url = "resource/%s/%s" % (self.id, filename)
    return url


class Resource(BaseModel):
    name = models.CharField(
        max_length=50, blank=True, verbose_name='nombre'
    )

    description = models.TextField(blank=True, verbose_name='descripción')

    url = models.URLField(blank=True)

    generic_url = models.TextField(blank=True, verbose_name='url genérica')

    image = models.FileField(upload_to=image_filename, null=True, blank=True)

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
