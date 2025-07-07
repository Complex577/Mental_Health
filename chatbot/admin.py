from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import ContentNode

class ContentNodeAdmin(admin.ModelAdmin):
    list_display = ('title_en', 'title_sw', 'node_type', 'level', 'parent')
    search_fields = ('title_en', 'title_sw', 'node_type')
    list_filter = ('node_type', 'level')
    ordering = ('node_type', 'level')

admin.site.register(ContentNode, ContentNodeAdmin)
