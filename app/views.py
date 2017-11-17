from django.shortcuts import render

from resources import models


def index(request):
    resources = models.Resource.objects.all()

    print(resources)

    return render(request, 'index.html', {'resources': resources})
