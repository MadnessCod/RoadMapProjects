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


class Category(BaseModel):
    name = models.CharField(max_length=100, null=False, blank=False, verbose_name='Name')

    class Meta:
        ordering = ('pk',)
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name


class Post(BaseModel):
    title = models.CharField(max_length=250, null=False, blank=False, verbose_name='Title')
    content = models.TextField(null=False, blank=False, verbose_name='Content')
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        verbose_name='Category',
        null=False,
        blank=False,
    )
    tags = models.ManyToManyField(
        'Tag',
        verbose_name='Tags',
        blank=True,
    )

    class Meta:
        ordering = ('pk',)
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'

    def __str__(self):
        return self.title
