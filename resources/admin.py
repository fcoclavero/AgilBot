from django.contrib import admin

# Register your models here.
from .models import Resource, Tag, Type

# Register your models here.
admin.site.register(Resource)
admin.site.register(Tag)
admin.site.register(Type)
