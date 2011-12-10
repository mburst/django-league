from django.conf.urls import patterns, url

urlpatterns = patterns('',
        url(r'^$', 'core.views.home', name='home'),
        url(r'^create_team/$', 'core.views.create_team', name='create-team'),
)
