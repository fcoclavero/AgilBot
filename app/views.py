from django.shortcuts import render

from resources import models


def index(request):
    resources = models.Resource.objects.all().order_by('-create_timestamp')
    weeks = models.Week.objects.all().order_by('-number')

    context = {
        'resources': resources,
        'weeks': weeks
    }
    return render(request, 'index.html', context)
