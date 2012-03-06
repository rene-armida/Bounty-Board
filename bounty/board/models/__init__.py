import settings

from django.db import models
import django.contrib.auth.models
from django.core.signals import request_started
from django.dispatch import receiver

# signals
@receiver(request_started)
def monkey_patch_redirect_uri(sender, **kwargs):
	'''
	Apply a cheesy hack to fix a glitch in social_auth: 
	* social_auth.backends.BaseOAuth2.__init__ calculates self.redirect_uri using request.build_absolute_uri
	* django.http.request.build_absolute_uri uses the scheme of the current request
	* if you're using heroku, or the app is behind a reverse proxy, all requests appear to be over HTTP, not HTTPS
	* thus all redirect_uris specified to the OAuth2 provider specify HTTP, causing problems

	This patch moves the 'redirect_uri' attrib to '_redirect_uri', and then substitutes a getter/setter combo
	to replace URLs starting with 'http://' with 'https://'.
	'''
	# print 'applying monkey patch...'
	import social_auth.backends
	import types
	def set_redirect_uri(self, redirect_uri):
		self._redirect_uri = redirect_uri
 
	def get_redirect_uri(self):
	    return self._redirect_uri.replace('http://', 'https://') if self._redirect_uri.startswith('http://') else self._redirect_uri

	social_auth.backends.BaseOAuth2.redirect_uri = property(get_redirect_uri, set_redirect_uri)

# models

class Hack(models.Model):
	'Represents a project or idea for collaborative effort at Hack Night events'
	name = models.CharField(max_length=50, help_text='Short name for this idea or project')
	abstract = models.CharField(max_length=150, help_text='A one-line description', blank=True)
	description = models.TextField(blank=True, help_text='Detailed description of your hack, project, or idea.  Use Markdown-style formatting.')
	source_url = models.URLField(verify_exists=False, help_text='Where to get the source code for this project', 
		blank=True)
	author = models.ForeignKey(django.contrib.auth.models.User, help_text='Proposer of this project')
	tags = models.ManyToManyField('Tag', blank=True)

	def __unicode__(self):
		return self.name

class Tag(models.Model):
	'Keywords that describe and group Hacks'
	name = models.CharField(max_length=40, unique=True)
	slug = models.SlugField(unique=True)

	def __unicode__(self):
		return self.name

	class Meta(object):
		ordering = ['name']