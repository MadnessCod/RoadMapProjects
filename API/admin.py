from django.contrib import admin
from django.contrib.admin import register
from .models import TodoList, User, Category


# Register your models here.

@register(TodoList)
class TodoListAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'author', 'description', 'category')
    list_display_links = ('id', 'title')
    list_filter = ('author', 'category')


@register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'email')
    list_display_links = ('id', 'name')


@register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
