from django.conf import settings
from django.shortcuts import render_to_response

def login(request):

	dest = settings.MEETUP_AUTHORIZATION_URL + \
		('?client_id=%s&response_type=code&redirect_uri=%s' % (settings.MEETUP_OAUTH2_CLIENT_ID, settings.MEETUP_REDIRECT_URI))
			
	return render_to_response(
		'login.html', 
		{
			'dest': dest,
		}
	)	