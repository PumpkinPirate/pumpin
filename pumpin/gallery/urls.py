from django.conf.urls import patterns, include, url

from pumpin.gallery.views import *

urlpatterns = patterns('',
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^edit/(?P<secret>[^/]+)/$', EditImageView.as_view(), name='edit'),
    url(r'^i/(?P<secret>[^/]+)/$', SumbittedImageView.as_view(), name='image_detail'),
    url(r'^i/(?P<secret>[^/]+)/report/$', ReportImageView.as_view(), name='report'),
    
    url(r'^moderate/$', ModerateView.as_view(), name='moderate'),
    url(r'^moderate/(?P<secret>[^/]+)/$', SetImageStatusView.as_view(), name='set_status'),
)
