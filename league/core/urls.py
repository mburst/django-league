from django.conf.urls import patterns, url

urlpatterns = patterns('',
        url(r'^$', 'core.views.home', name='home'),
        url(r'^manage_team/(?P<team_id>\d+)/$', 'core.views.manage_team', name='manage-team'),
        url(r'^player_search/$', 'core.views.player_search', name='player-search'),
        
        #League
        url(r'^league/(?P<league_id>\d+)/division/SOMETHINGHERE/create_team/$', 'core.views.create_team', name='create-team'),
)
