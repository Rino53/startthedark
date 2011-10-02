from django.conf.urls.defaults import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^events/', include('events.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
