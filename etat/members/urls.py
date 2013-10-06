from django.conf.urls import patterns, url

from .views import *

urlpatterns = patterns('',
    url(r'^$',
        members_list,
        name='members_list'
    ),
)
