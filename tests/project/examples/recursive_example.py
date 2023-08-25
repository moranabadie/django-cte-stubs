"""An example with recursion."""
from typing import TYPE_CHECKING, TypedDict

import django
from django.db.models import F, IntegerField, TextField, Value
from django.db.models.functions import Concat
from django_cte import With

if TYPE_CHECKING:
    from django.db.models.query import _QuerySet
    from django_stubs_ext import WithAnnotations

django.setup()

from myapp.models import Order, Region  # noqa: E402

Order.objects.all().delete()
Region.objects.all().delete()
region = Region.objects.create(name="example")
Order.objects.create(amount=2, region=region)
region2 = Region.objects.create(name="example2", region=region)
Order.objects.create(amount=2, region=region2)


class RegionInfo(TypedDict):
    """Annotation of a region."""

    name: str


class RecRegionInfo(TypedDict):
    """Annotation of a region."""

    path: str
    depth: int


def make_regions_cte(cte: "With[Region]") -> "_QuerySet[Region, RegionInfo]":
    """Set the recursion."""
    # non-recursive: get root nodes
    return Region.objects.filter(
        parent__isnull=True,
    ).values(
        "name",
        path=F("name"),
        depth=Value(0, output_field=IntegerField()),
    ).union(
        # recursive union: get descendants
        cte.join(Region, parent=cte.col.name).values(
            "name",
            path=Concat(
                cte.col.path, Value(" / "), F("name"),
                output_field=TextField(),
            ),
            depth=cte.col.depth + Value(1, output_field=IntegerField()),
        ),
        all=True,
    )


cte: "With[Region]" = With.recursive(make_regions_cte)

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

r: "WithAnnotations[Order, RecRegionInfo]" = regions.get()
path: str = r.path
