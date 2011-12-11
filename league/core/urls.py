from django.conf.urls import patterns, url

urlpatterns = patterns('',
        url(r'^$', 'core.views.home', name='home'),
        url(r'^create_team/$', 'core.views.create_team', name='create-team'),
        url(r'^manage_team/(?P<team_id>\d+)/$', 'core.views.manage_team', name='manage-team'),
        url(r'^player_search/$', 'core.views.player_search', name='player-search'),
)
