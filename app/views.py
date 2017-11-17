from django.http import Http404
from django.shortcuts import render

from resources import models


def index(request):
    resources = models.Resource.objects.all().order_by('-create_timestamp')
    weeks = models.Week.objects.all().order_by('-number')

    context = {
        'resources': resources,
        'weeks': weeks,
        'section': 'all',
        'section_text': 'Todos'
    }
    return render(request, 'index.html', context)


def week_view(request, id):
    if not models.Week.objects.filter(id=id):
        raise Http404('No existe esa semana')

    week = models.Week.objects.get(id=id)
    resources = models.Resource.objects.filter(weeks=week).order_by('-create_timestamp')
    weeks = models.Week.objects.all().order_by('-number')

    context = {
        'resources': resources,
        'weeks': weeks,
        'section': id,
        'section_text': week.name
    }
    return render(request, 'index.html', context)
