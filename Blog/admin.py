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
    list_display = ('id', 'title', 'content')
    search_fields = ('title',)
