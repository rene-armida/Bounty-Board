import django.db.models
from django.conf.urls.defaults import patterns, include, url
from django.shortcuts import redirect
from bounty.board import models
import bounty.board.api as api
#import django.contrib.auth.views

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

# REST resources
hack_resource = api.HackResource()

urlpatterns = patterns('bounty.board.views',
    url(r'^$', 'home.home'),
    #url(r'^$', redirect('home')),
    
    # RESTful API
    url(r'^api/', include(hack_resource.urls)),

    # for Meetup API 
    url(r'', include('social_auth.urls')),

    # standard django admin
    url(r'^admin/', include(admin.site.urls)),

    # debugging - remove me
    url(r'^accounts/profile', 'debug.dump_user_info'),   
)

urlpatterns += patterns('',
    # debugging - remove me
    url(r'^accounts/login/$', 'django.contrib.auth.views.login', {'template_name': 'login.html'}),
)