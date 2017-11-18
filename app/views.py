from django.shortcuts import render

from resources import models
from itertools import chain

def index(request):
    resources = models.Resource.objects.all()

    print(resources)

    return render(request, 'index.html', {'resources': resources})


def search(request, words):
    # resources = models.Resource.objects.filter()
    resources = models.Resource.objects.all()
    none_qs = models.Resource.objects.none()
    for word in words.split(" "):
        queryset = models.Resource.objects.filter(description__contains=word)
        none_qs = none_qs | queryset

    return render(request, 'index.html', {'resources': none_qs, 'query': words})
