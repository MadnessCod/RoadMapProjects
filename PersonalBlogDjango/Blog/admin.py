from django.contrib import admin
from django.contrib.admin import register

from .models import Article


# Register your models here.

@register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'author',)
    list_filter = ('author',)
