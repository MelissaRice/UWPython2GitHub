from django.conf.urls.defaults import *
from django.conf import settings

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Recipes
    (r'^recipes/',include('recipes.urls')),

    # Json Polls API
    #(r'^jrecipes/', include('jrecipes.urls')),

    # Admin docs
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Admin:
    (r'^admin/', include(admin.site.urls)),

    # Site Media
    (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    
    # Default:
    (r'^$', 'views.index')
)

handler404 = 'views.error404'
