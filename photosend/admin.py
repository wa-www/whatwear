from django.contrib import admin

# Register your models here.

from .models import Photo
from .models import Comment


# class PhotoAdmin(admin.ModelAdmin):
#     fields = ['title', 'content','photo','created_at']

# admin.site.register(Photo, PhotoAdmin)

class PhotoAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'photo')
    list_display_links = ('id', 'title', 'photo')

admin.site.register(Photo, PhotoAdmin)

class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'comment')
    list_display_links = ('id', 'comment')

admin.site.register(Comment, CommentAdmin)