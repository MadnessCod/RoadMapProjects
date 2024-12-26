from django.contrib import admin
from django.contrib.admin import register
from .models import Tag, Post


# Register your models here.

@register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name')
    search_fields = ('name',)


@register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'tags')
    search_fields = ('title', 'tags')
    list_filter = ('tags',)
