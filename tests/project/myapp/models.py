"""Some models to test with."""

from __future__ import annotations

from django.db import models


class Author(models.Model):
    """An author."""

    name = models.CharField(max_length=100)

    def __str__(self) -> str:
        """Return a dummy string."""
        return f"An author: {self.name}"


class Book(models.Model):
    """A book."""

    title = models.CharField(max_length=100)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    published_date = models.DateField(auto_now_add=True)
    nb_line = models.IntegerField(default=1)

    def __str__(self) -> str:
        """Return a dummy string."""
        return f"A book: {self.title}"


class Region(models.Model):
    """A region."""

    name = models.TextField(primary_key=True)
    parent = models.ForeignKey("self", null=True, on_delete=models.CASCADE)

    class Meta:
        """The region meta."""

        db_table = "region"

    def __str__(self) -> str:
        """Return a dummy string."""
        return f"A region: {self.name}"


class Order(models.Model):
    """An order."""

    amount = models.IntegerField()
    region = models.ForeignKey("Region", on_delete=models.CASCADE)

    class Meta:
        """The order meta."""

        db_table = "orders"

    def __str__(self) -> str:
        """Return a dummy string."""
        return f"An order: {self.pk}"
