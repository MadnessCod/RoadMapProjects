from django.contrib import admin
from django.contrib.admin import register
from .models import TodoList


# Register your models here.

@register(TodoList)
class TodoListAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'description')
    list_display_links = ('id', 'title')
