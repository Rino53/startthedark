from django.conf.urls.defaults import patterns, include, url
from events import views

urlpatterns = patterns('',

    url(r'^create/$', views.create, name='ev_create'),
    url(r'^tonight/$', views.tonight, name='ev_tonight'),
    url(r'^toggle-attendance/$', views.toggle_attendance, name='ev_toggle_attendance'),
)
