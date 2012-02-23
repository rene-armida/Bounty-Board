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


urlpatterns = patterns('bounty.board.views',
    url(r'^$', 'home.home'),
    #url(r'^$', redirect('home')),
    
    # RESTful API
    url(r'^api/hacks$', ListOrCreateModelView.as_view(resource=HackResource)),

    # standard django admin
    url(r'^admin/', include(admin.site.urls)),
)
