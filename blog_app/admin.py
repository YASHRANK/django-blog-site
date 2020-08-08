from django.contrib import admin
from .models import Post, Comment 

from tinymce.widgets import TinyMCE
from django.db import models

from django.utils.translation import ngettext
from django.contrib import messages
# Register your models here.



class PostAdmin(admin.ModelAdmin):
    
    actions = ['make_published', 'make_unpublished']
  
    list_display = ('title','is_published', 'author', 'created_at')
    search_fields = ('slug',  )
    formfield_overrides = { models.TextField: {'widget': TinyMCE(mce_attrs={'height': 550,'width': 1000})}, }
    prepopulated_fields = {'slug': ('title',)}

    def make_published(self, request, queryset):
        updated = queryset.update(is_published=True)
        self.message_user(request, ngettext(
            '%d story was successfully marked as published.',
            '%d stories were successfully marked as published.',
            updated,
        ) % updated, messages.SUCCESS)
    make_published.short_description = "Mark as Published"

    def make_unpublished(self, request, queryset):
            updated = queryset.update(is_published='False')
            self.message_user(request, ngettext(
            '%d story was successfully marked as unpublished.',
            '%d stories were successfully marked as unpublished.',
            updated,
        ) % updated, messages.WARNING)
    make_unpublished.short_description = "Mark as Unpublished"

admin.site.register(Post , PostAdmin)


class CommentAdmin(admin.ModelAdmin):
  
    list_display = ('user','body', 'created_at')
    search_fields = ['user__username']

admin.site.register(Comment,CommentAdmin)
