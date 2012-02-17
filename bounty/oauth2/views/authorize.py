from django.http import HttpResponseBadRequest
from django.views.generic import RedirectView
from dzen.django.apps.common.views import ProtectedViewMixin
from oauth2.exceptions import *
from oauth2.provider import OAuth2Provider
from oauth2.views import OAuth2DispatchView, OAuth2ViewMixin

class AuthorizeView(OAuth2ViewMixin, RedirectView):
    permanent = False
    response_type = 'code'

    def dispatch_request(self, request, *args, **kwargs):
        response = super(AuthorizeView, self).dispatch_request(request, *args, **kwargs)
        self.url = self.provider.get_redirect_url(response, getattr(self, 'implicit_grant', False))

    def get(self, request, *args, **kwargs):
        self.dispatch_request(request, *args, **kwargs)
        return super(AuthorizeView, self).get(request, *args, **kwargs)

    def oauth2_request(self, request):
        return self.provider.request_authorization(
                request.user,
                request.REQUEST.get('scope', ''),
                self.response_type,
                request.REQUEST.get('state', '')
                )

class ImplicitAuthorizeView(AuthorizeView):
    response_type = 'token'
    implicit_grant = True

class AuthorizeViewDispatcher(ProtectedViewMixin, OAuth2DispatchView):
    '''
    This view is a "dispatcher" in that it doesn't actually return a HttpResponse;
    it implements 'get' to build the appropriate view, based on inspecting
    request attribs, and then returns that view's response.

    ProtectedViewMixin: equivalent to all methods having @method_decorator(login_required) applied
    OAuth2DispatchView: inherits from class-based generic View.
    '''
    dispatch_views = {
            AuthorizeView.response_type: AuthorizeView,
            ImplicitAuthorizeView.response_type: ImplicitAuthorizeView,
            }

    def get(self, request, *args, **kwargs):
        'Delegated to by View.dispatch; call OAuth2DispatchView.dispatch_request'
        return self.dispatch_request(request, *args, **kwargs)

    def get_provider(self, request):
        return OAuth2Provider(
                request.REQUEST.get('client_id'),
                redirect_uri=request.REQUEST.get('redirect_uri')
                )

    def handle_provider_error(self, request, ex):
        if not isinstance(ex, OAuth2Error):
            raise

        return HttpResponseBadRequest(ex.message)

    def get_dispatch_key(self, request):
        return request.REQUEST.get('response_type', 'code')
