from django.db import models


class Bot(models.Model):
    name = models.CharField(max_length=100, verbose_name='Nombre')
    token = models.CharField(max_length=255)

    def __str__(self):
        return str(self.name)

    @classmethod
    def get_token(cls):
        return str(Bot.objects.all().first().token)
