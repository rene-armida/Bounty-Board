from distutils.core import setup
from dzen import __version__

setup(
        name='DZ Common Web',
        description='Common apps for creating DZ websites',
        version=__version__,
        author='Craig Slusher',
        author_email='craig@disorderlyzen.com',
        packages=[
        	'dzen', 
        	'dzen.django', 
        	'dzen.django.apps', 
        	'dzen.django.apps.common', 
        	'dzen.django.apps.common.decorators',
        	'dzen.django.apps.common.templatetags',
        	'dzen.django.apps.error',
        	'dzen.django.apps.smashed',
        	'dzen.django.apps.smashed.templatetags',
        	'dzen.django.serializers',
    	],
)
