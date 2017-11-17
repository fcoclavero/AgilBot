from django.shortcuts import render

from resources import models


def index(request):
    resources = models.Resource.objects.all().order_by('-create_timestamp')

    print(resources)

    return render(request, 'index.html', {'resources': resources})
