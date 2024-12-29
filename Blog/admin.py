from django.contrib import admin
from django.contrib.admin import register
from .models import Tag, Category, Post


# Register your models here.

@register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name')
    search_fields = ('name',)


@register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name')
    search_fields = ('name',)


@register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'content', 'category', 'display_tags')
    search_fields = ('title',)

    def display_tags(self, obj):
        return ', '.join(tag.name for tag in obj.tags.all())
    display_tags.short_description = 'Tags'
