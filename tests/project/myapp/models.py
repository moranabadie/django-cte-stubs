"""Some models to test with."""
from django.db import models
from django_cte import CTEManager, CTEQuerySet


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
    objects: CTEManager = CTEManager()

    def __str__(self) -> str:
        """Return a dummy string."""
        return f"A book: {self.title}"


class Region(models.Model):  # type: ignore[django-manager-missing]
    """A region."""

    name = models.TextField(primary_key=True)
    parent = models.ForeignKey("self", null=True, on_delete=models.CASCADE)
    objects: CTEManager = CTEManager()

    class Meta:
        """The region meta."""

        db_table = "region"

    def __str__(self) -> str:
        """Return a dummy string."""
        return f"A region: {self.name}"


class LargeOrdersQuerySet(CTEQuerySet["Order"]):
    """Manager orders."""

    def example(self) -> "LargeOrdersQuerySet":
        """Define a custom query filter."""
        return self.filter(amount__gt=100)


class Order(models.Model):
    """An order."""

    large = LargeOrdersQuerySet.as_manager()
    amount = models.IntegerField()
    region = models.ForeignKey("Region", on_delete=models.CASCADE)
    objects = LargeOrdersQuerySet.as_manager()


    class Meta:
        """The order meta."""

        db_table = "orders"


    def __str__(self) -> str:
        """Return a dummy string."""
        return f"An order: {self.pk}"
