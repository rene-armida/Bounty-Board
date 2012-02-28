from django.contrib import admin
from bounty.board import models

class TagAdmin(admin.ModelAdmin):
	prepopulated_fields = {
		'slug': ('name', ),
	}

admin.site.register(models.Tag, TagAdmin)
admin.site.register(models.Hack)