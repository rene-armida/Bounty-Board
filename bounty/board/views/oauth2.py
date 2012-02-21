from django.conf import settings
import django.http
from django.shortcuts import render_to_response

import json
import urllib
import urllib2


def require_https(fn):
	'''
	decorate a view to raise 403 (forbidden) if we're not connected via HTTPS

	replace this with 'raise Http403' when that gets released
	see: https://docs.djangoproject.com/en/dev/topics/http/views/#the-403-http-forbidden-view
	'''
	def protected_view(request):
		if not request.is_secure():
			return django.http.HttpResponse(status=403, content='Forbidden')
		# otherwise, invoke the view as usual
		return fn(request)
	return protected_view

def login(request):
	dest = settings.MEETUP_AUTHORIZATION_URL + \
		('?client_id=%s&response_type=code&redirect_uri=%s' % (settings.MEETUP_OAUTH2_CLIENT_ID, settings.MEETUP_REDIRECT_URI))

	return render_to_response(
		'login.html', 
		{
			'dest': dest,
		}
	)

@require_https
def authorize(request):
	'''
	receive an auth code from Meetup; store the auth code and state
	'''
	if 'error' in request.GET:
		# this authorization request was not successful
		if request.GET['error'] == 'access_denied':
			# the meetup user denied us; explain this on our end
			return render_to_response('access_denied.html')
		
		# otherwise, there must be a programming or setup error; 
		# raise an Exception describing the problem, so it gets logged
		raise Exception('Meetup authorization failed; error: %s' % request.GET['error'])

	# we were successfully authorized, post to the Meetup token endpoint
	post_data = urllib.urlencode({
		'client_id': settings.MEETUP_OAUTH2_CLIENT_ID,
		'grant_type': 'authorization_code',
		'redirect_uri': settings.MEETUP_REDIRECT_URI,
		'code': request.GET['code'],
	})
	# note: urllib2.urlopen doesn't verify server's cert; is this a security hole?
	response = urllib2.urlopen(settings.MEETUP_TOKEN_URL, post_data)

	# interpret the response as JSON content; both success and failure use this response type
	# if a lower-level failure occurred, like the connection not being made, we assume urlopen
	# will have raised a URLError.
	response = json.loads(response)
	if 'error' in response:
		raise Exception('Meetup access token request failed: %s' % response['error'])
	
	return django.http.HttpResponse(content='access token: %s; refresh token: %s' % (response['access_token'], response['refresh_token']))