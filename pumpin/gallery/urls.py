from django.conf.urls import patterns, include, url

from pumpin.gallery.views import IndexView

urlpatterns = patterns('',
    url(r'^$', IndexView.as_view(), name='index'),
)
