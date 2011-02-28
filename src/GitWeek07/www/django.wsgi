import os, sys
from django.core.handlers.wsgi import WSGIHandler

sys.path.append('/home/mlrice/www')
sys.path.append('/home/mlrice/www/dtest')

os.environ['DJANGO_SETTINGS_MODULE'] = 'dtest.settings'
application = WSGIHandler()


