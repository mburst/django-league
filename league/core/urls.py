from django.conf.urls import patterns, url

urlpatterns = patterns('',
        url(r'^$', 'core.views.home', name='home'),
)
