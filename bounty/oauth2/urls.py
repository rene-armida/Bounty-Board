from django.conf.urls.defaults import patterns, include, url
from oauth2.views.authorize import AuthorizeViewDispatcher
from oauth2.views.token import TokenViewDispatcher

urlpatterns = patterns('',
        url(r'^authorize/$', AuthorizeViewDispatcher.as_view(), name='authorize'), # as_view comes from class-based View.as_view
        url(r'^token/$', TokenViewDispatcher.as_view(), name='token'),
        )
