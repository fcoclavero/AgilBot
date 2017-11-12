from django.contrib import admin

# Register your models here.
from .models import Resource, Tag, Type


admin.site.site_title = 'Recursos'
admin.site.site_header = 'Recursos'

class ResourceAdmin(admin.ModelAdmin):
    model = Resource
    readonly_fields = ('create_timestamp', 'update_timestamp')


class TagAdmin(admin.ModelAdmin):
    model = Tag
    readonly_fields = ('create_timestamp', 'update_timestamp')


class TypeAdmin(admin.ModelAdmin):
    model = Type
    readonly_fields = ('create_timestamp', 'update_timestamp')

# Register your models here.
admin.site.register(Resource, ResourceAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Type, TypeAdmin)
