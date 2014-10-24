from django.conf.urls import patterns, include, url
from django.contrib import admin
from hunts.api_views import UsersView, TreasureHuntsView

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'bittreasure.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url('^api/users/$', UsersView.as_view(), name='api_users'),
    url('^api/users/login/$', 'hunts.api_views.login', name='api_user_login'),
    url('^api/users/logout/$', 'hunts.api_views.logout', name='api_user_logout'),
    url('^api/treasurehunts/$', TreasureHuntsView.as_view(), name='api_treasurehunts_view'),

    url(r'^admin/', include(admin.site.urls)),
)
