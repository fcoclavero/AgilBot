# App urls
from django.conf.urls import url

from app import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^semana/(?P<id>\d+)/$', views.week_view, name='week_view'),
    url(r'^search/(?P<words>.+)/$', views.search, name='search'),
]
