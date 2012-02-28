import settings

from django.db import models
import django.contrib.auth.models

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