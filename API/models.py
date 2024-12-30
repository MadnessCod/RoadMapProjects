from django.db import models


# Create your models here.

class BaseMode(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ('-created_at',)

    def __str__(self):
        return NotImplemented('str method not implemented')


class TodoList(BaseMode):
    title = models.CharField(max_length=255)
    description = models.TextField()

    class Meta:
        verbose_name = 'Todo List'
        verbose_name_plural = 'Todo Lists'
        ordering = ('pk',)

    def __str__(self):
        return self.title

