from django.contrib import admin
from django.contrib.admin import register

from .models import Expense


# Register your models here.

@register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'amount')
    list_filter = ('category', 'amount')
    search_fields = ('category', 'amount')
