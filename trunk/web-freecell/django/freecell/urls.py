#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf.urls.defaults import *

urlpatterns = patterns('mysite.freecell.views',
    (r'^$', 'index'),
    (r'^(?P<seed>\d+)/$', 'detail'),
    (r'^(?P<seed>\d+)/results/$', 'results'),
    (r'^(?P<seed>\d+)/vote/$', 'vote'),
)
