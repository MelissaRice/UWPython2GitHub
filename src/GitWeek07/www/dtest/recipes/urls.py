'''
Created on Feb 23, 2011

@author: mlr
'''

from django.conf.urls.defaults import *

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('recipes.views',
    (r'^$', 'index'),
    (r'^(?P<recipe_id>\d+)/$', 'detail'),
    (r'ingredient/(?P<ingredient_name>\w+)/$', 'ingredient'),
    (r'tags/$', 'tags'),
    (r'tags/(?P<tag_name>\w+)/$', 'tagged'),
)
