from django.conf.urls import patterns, include, url
from django.conf import settings

from pumpin.gallery.views import *

urlpatterns = patterns('',
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^edit/(?P<secret>[^/]+)/$', EditImageView.as_view(), name='edit'),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT,
        }),
   )