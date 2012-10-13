from django.conf.urls import patterns, include, url

from pumpin.gallery.views import *

urlpatterns = patterns('',
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^edit/(?P<secret>[^/]+)/$', EditImageView.as_view(), name='edit'),
    url(r'(?P<secret>[^/]+)/$', SumbittedImageView.as_view(), name='image_detail'),
)
