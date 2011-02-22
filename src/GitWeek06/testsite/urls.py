from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Polls
    (r'^polls/',include('polls.urls')),

    # Json Polls API
    (r'^jpolls/', include('jpolls.urls')),

    # Admin docs
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Admin:
    (r'^admin/', include(admin.site.urls)),

    # Default:
    (r'^$', 'views.index')
)

handler404 = 'views.error404'
