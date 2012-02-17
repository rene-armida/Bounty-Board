from django.conf.urls.defaults import patterns, include, url
from django.shortcuts import redirect
from djangorestframework.resources import ModelResource
from djangorestframework.views import ListOrCreateModelView, InstanceModelView
from bounty.oauth2.views.authorize import AuthorizeViewDispatcher
from bounty.oauth2.views.token import TokenViewDispatcher


# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('bounty.board.views',
    url(r'^$', 'home.home'),
    #url(r'^$', redirect('home')),
    # Examples:
    # url(r'^app/', include('app.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),

    # oauth2 urls
    # todo: maybe move to a separate urlconf
    url(r'^authorize/$', AuthorizeViewDispatcher.as_view(), name='authorize'),
    url(r'^token/$', TokenViewDispatcher.as_view(), name='token'),

)
