import os
import sys
import site

#virtualenv
site.addsitedir('/path/to/pumpin/lib/python2.7/site-packages')
sys.path.append('/path/to/pumpin/')
os.environ['DJANGO_SETTINGS_MODULE'] = 'pumpin.settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
