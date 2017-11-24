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


def week_view(request, pk):
    if not models.Week.objects.filter(id=pk):
        raise Http404('No existe esa semana')

    week = models.Week.objects.get(id=pk)
    resources = models.Resource.objects.filter(weeks=week).order_by('-create_timestamp')
    weeks = models.Week.objects.all().order_by('-number')

    context = {
        'resources': resources,
        'weeks': weeks,
        'section': pk,
        'section_text': week.name
    }
    return render(request, 'index.html', context)


def search(request, words):
    none_qs = models.Resource.objects.none()
    for word in words.split(" "):
        queryset = models.Resource.objects.filter(description__contains=word)
        none_qs = none_qs | queryset

    return render(request, 'index.html', {'resources': none_qs})
