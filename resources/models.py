from django.db import models


# Create your models here.
class Resource(models.Model):

    name = models.CharField(max_length=50, blank=True, verbose_name='nombre')
    url = models.CharField(max_length=100, blank=False)
    create_timestamp = models.DateTimeField(
        auto_now_add=True, editable=False, verbose_name='Fecha de creación'
    )
    update_timestamp = models.DateTimeField(
        auto_now=True, editable=False, verbose_name='Fecha de modificación'
    )

    class Meta:
        verbose_name = 'Recurso'
        verbose_name_plural = 'Recursos'

    def __str__(self):
        return self.name + ': ' + self.url
