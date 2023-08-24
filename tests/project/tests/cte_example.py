"""Some simple checks."""
from typing import TYPE_CHECKING, TypedDict

import django
from django.db.models import Sum
from django_cte import CTEQuerySet, With

django.setup()

from myapp.models import Author, Book  # noqa: E402

if TYPE_CHECKING:
    from django_stubs_ext import WithAnnotations


class NotaBook(TypedDict):

    """book annotations."""

    author_total: int


wrong_cte_1: "With[Book]" = With(
    Author.objects.all(),  # type: ignore[arg-type]   # it should be a Book query not an Author
)

good_cte_1: "With[Book]" = With(
    Book.objects.all(),
)

good_cte_2: "With[Book]" = With(
    Book.objects
    .values("author_id"),
)

cte: "With[Book]" = With(
    Book.objects
    .values("author_id")
    .annotate(total=Sum("nb_line")),
)

wrong_cte: int = cte  # type: ignore[assignment]  # it should fail, wrong type

good_queryset: CTEQuerySet[Book] = cte.queryset()
bad_queryset: CTEQuerySet[Author] = cte.queryset()  # type: ignore[assignment]  # it should be a Book not an Author

orders: "CTEQuerySet[WithAnnotations[Book, NotaBook]]" = (
    # FROM orders INNER JOIN cte ON orders.region_id = cte.region_id
    cte.join(Book, author=cte.col.author_id)

    # Add `WITH ...` before `SELECT ... FROM orders ...`
    .with_cte(cte)

    # Annotate each Order with a "region_total"
    .annotate(author_total=cte.col.total)
)

wrong_get: int = orders.get()  # type: ignore[assignment]
wrong_author_total: str = orders.get().not_author_total  # type: ignore[attr-defined]
ok_author_total: int = orders.get().author_total
wrong_author_total_2: str = orders.get().author_total  # type: ignore[assignment]

wrong_title: int = orders.get().title  # type: ignore[assignment]
ok_title: str = orders.get().title
