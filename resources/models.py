from django.db import models


# Create your models here.
class Resource(models.Model):

    name = models.CharField(max_length=50, blank=True, verbose_name='nombre')
    url = models.CharField(max_length=100, blank=False)

    class Meta:
        verbose_name = 'Recurso'
        verbose_name_plural = 'Recursos'

    def __str__(self):
        return self.name
