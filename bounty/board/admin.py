from django.contrib import admin
from bounty.board import models

admin.site.register(models.Tag)
admin.site.register(models.Hack)