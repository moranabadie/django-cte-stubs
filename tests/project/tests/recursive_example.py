"""An example with recursion."""

from typing import TYPE_CHECKING, TypedDict

import django
from django.db.models import F, IntegerField, TextField, Value
from django.db.models.functions import Concat
from django_cte import CTEQuerySet, With

if TYPE_CHECKING:
    from django.db.models.query import _QuerySet

django.setup()

from myapp.models import Book, Region  # noqa: E402


class RegionInfo(TypedDict):
    """Annotation of a region."""

    name: str


def make_regions_cte(cte: "With[Region]") -> "_QuerySet[Region, RegionInfo]":
    """Set the recursion."""
    # non-recursive: get root nodes
    return (
        Region.objects.filter(
            parent__isnull=True,
        )
        .values(
            "name",
            path=F("name"),
            depth=Value(0, output_field=IntegerField()),
        )
        .union(
            # recursive union: get descendants
            cte.join(Region, parent=cte.col.name).values(
                "name",
                path=Concat(
                    cte.col.path,
                    Value(" / "),
                    F("name"),
                    output_field=TextField(),
                ),
                depth=cte.col.depth + Value(1, output_field=IntegerField()),
            ),
            all=True,
        )
    )


cte: "With[Region]" = With.recursive(make_regions_cte)

# it should be a Region query not an Book
wrong_cte: "With[Book]" = With.recursive(make_regions_cte)  # type: ignore[arg-type]

regions = (
    cte.join(Region, name=cte.col.name)
    .with_cte(cte)
    .annotate(
        path=cte.col.path,
        depth=cte.col.depth,
    )
    .filter(depth=2)
    .order_by("path")
)

orders_wrong: int = cte.queryset().with_cte(cte)  # type: ignore[assignment]
orders_ok: "CTEQuerySet[Region]" = cte.queryset().with_cte(cte)
