from django.db import models


# Create your models here.

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ('-created_at',)


class Tag(BaseModel):
    name = models.CharField(max_length=100, null=False, blank=False, verbose_name='Name')

    class Meta:
        ordering = ('pk',)
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'

    def __str__(self):
        return self.name


class Post(BaseModel):
    title = models.CharField(max_length=250, null=False, blank=False, verbose_name='Title')
    content = models.TextField(null=False, blank=False, verbose_name='Content')
    tags = models.ForeignKey(
        'Tag',
        verbose_name='Tags',
        null=True,
        blank=True,
        on_delete=models.CASCADE
    )
