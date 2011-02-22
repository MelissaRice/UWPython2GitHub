from django.conf.urls.defaults import *

urlpatterns = patterns('jpolls.views',

    # Json Poll Stuff
    
    # API instructions
    (r'api/$', 'api'),

    # Poll index page
    (r'^$', 'index'),
    
    # Poll detail page by poll id
    (r'^(?P<poll_id>\d+)/$', 'detail'),
    
    # Poll results page by poll id: to see the outcome of the poll (vote tally)
    (r'^(?P<poll_id>\d+)/results/$', 'results'),

    # Poll voting page by poll id
    (r'^(?P<poll_id>\d+)/vote/(?P<choice_id>\d+)$', 'vote'),
    
)

