from django.db import models


# Create your models here.

class Book(models.Model):
    name = models.CharField(max_length=256)
    authors = models.ManyToManyField('example_app.Author')
    publication = models.ForeignKey(
        'example_app.Publication', null=True, on_delete=models.SET_NULL, related_name='published_books')
    published_date = models.DateTimeField(null=True, auto_now_add=True, auto_now=False)

    class Meta:
        app_label = 'example_app'


class Publication(models.Model):
    name = models.CharField(max_length=128)
    address = models.TextField(null=True)

    class Meta:
        app_label = 'example_app'


class Author(models.Model):
    user = models.OneToOneField('auth.User', on_delete=models.CASCADE, related_name='author', null=True, default=None)
    name = models.CharField(max_length=128)
    address = models.TextField(null=True)

    class Meta:
        app_label = 'example_app'


