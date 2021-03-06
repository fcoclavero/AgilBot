from django.contrib import admin
from .models import Resource, Tag, Type, Week, Semester

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


class WeekInlineAdmin(admin.TabularInline):
    model = Week


class WeekAdmin(admin.ModelAdmin):
    model = Week


class SemesterAdmin(admin.ModelAdmin):
    model = Semester
    inlines = (WeekInlineAdmin,)


# Register your models here.
admin.site.register(Resource, ResourceAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Type, TypeAdmin)
admin.site.register(Week, WeekAdmin)
admin.site.register(Semester, SemesterAdmin)
