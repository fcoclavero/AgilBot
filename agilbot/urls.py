# Project urls
from django.conf.urls import url, include
from django.contrib import admin
from django.conf.urls.static import static

from agilbot import settings

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^bot/', include('bot.urls', namespace='bot')),
    url(r'^', include('app.urls', namespace='app')),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
