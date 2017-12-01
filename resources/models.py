from django.utils import timezone
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
        verbose_name='section'
    )
    chat_id = models.IntegerField(
        verbose_name='chat ID'
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
    start_date = models.DateField(verbose_name='Fecha de inicio')

    end_date = models.DateField(verbose_name='Fecha de termino')

    class Meta:
        verbose_name = 'Semana'
        verbose_name_plural = 'Semanas'

    def __str__(self):
        return self.name + ' ' + str(self.number)


class Tag(BaseModel):
    name = models.CharField(
        max_length=50, blank=True, verbose_name='nombre'
    )

    class Meta:
        verbose_name = 'Etiqueta'
        verbose_name_plural = 'Etiquetas'

    def __str__(self):
        return self.name

    @staticmethod
    def transform_name(name):
        separators = [' ', '-', '_', '.', ',']
        if any(s in name for s in separators):
            for s in separators[1:]:
                name = name.replace(s, ' ')
            name = name.title()
            name = name.replace(' ', '')

        if name[0] != '#':
            name = '#' + name

        if len(name) > 2:
            name = name[0] + name[1].upper() + name[2:]
        return name

    @staticmethod
    def find_or_create_tag(name):
        transformed_name = Tag.transform_name(name)
        tag = Tag.objects.filter(name=transformed_name).first()
        if tag is None:
            tag = Tag.objects.create(name=transformed_name)
        return tag

    def save(self, *args, **kwargs):
        self.name = Tag.transform_name(str(self.name))
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

    publication_date = models.DateField(
        blank=True, null=True,
        verbose_name='Fecha de publicación'
    )

    class Meta:
        verbose_name = 'Recurso'
        verbose_name_plural = 'Recursos'

    def __str__(self):
        return self.name + ': ' + self.url

    def save(self, *args, **kwargs):
        if self.publication_date is None:
            self.publication_date = timezone.localtime(timezone.now())
        super(Resource, self).save(*args, **kwargs)
