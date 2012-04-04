import django.db.models
from django.conf.urls.defaults import patterns, include, url
from django.shortcuts import redirect
from bounty.board import models
from djangorestframework.resources import ModelResource
from djangorestframework.views import ListOrCreateModelView, InstanceModelView

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

# REST resources
class HackResource(ModelResource):
    model = models.Hack
    # by default, exclude is ('id', 'pk'); we want ID exposed
    exclude = []

urlpatterns = patterns('bounty.board.views',
    url(r'^$', 'home.home'),
    #url(r'^$', redirect('home')),
    
    # RESTful API
    url(r'^api/hacks$', ListOrCreateModelView.as_view(resource=HackResource)),

    # for Meetup API 
    url(r'', include('social_auth.urls')),

    # standard django admin
    url(r'^admin/', include(admin.site.urls)),

    # debugging - remove me
    url(r'^accounts/profile', 'debug.dump_user_info'),
)
