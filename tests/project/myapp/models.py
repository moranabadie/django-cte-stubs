from django.db import models
from django_cte import CTEManager


class Author(models.Model):
    name = models.CharField(max_length=100)


class Book(models.Model):
    objects = CTEManager()
    title = models.CharField(max_length=100)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    published_date = models.DateField()
    nb_line = models.IntegerField(default=1)
