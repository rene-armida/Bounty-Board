import pprint
from django.http import HttpResponse

def _dump(obj):
	return pprint.pformat(obj.__dict__)

def dump_user_info(request):
	return HttpResponse(
		"""Logged in user: 
%s

Session:
%s
""" % (_dump(request.user), _dump(request.session)), content_type='text/plain'
	)
