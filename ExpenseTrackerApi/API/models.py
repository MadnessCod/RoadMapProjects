from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ['-created_at', ]

    def __str__(self):
        return NotImplemented('str method not implemented')


class Expense(BaseModel):
    CATEGORY_CHOICES = [
        ('GROCERIES', 'Groceries'),
        ('LEISURE', 'Leisure'),
        ('ELECTRONICS', 'Electronics'),
        ('UTILITIES', 'Utilities'),
        ('CLOTHING', 'Clothing'),
        ('HEALTH', 'Health'),
        ('OTHERS', 'Others'),
    ]
    name = models.CharField(max_length=255, verbose_name='name')
    description = models.TextField(verbose_name='description')
    amount = models.FloatField(verbose_name='amount')

    category = models.CharField(
        max_length=64,
        choices=CATEGORY_CHOICES,
        default='OTHER',
    )

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        verbose_name='user')

    class Meta:
        verbose_name = 'Expense'
        verbose_name_plural = 'Expenses'
        ordering = ['pk', ]

    def __str__(self):
        return f'{self.name} - ${self.amount} - {self.get_category_display()}'
