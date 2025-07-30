"""Tests named CTEs."""

from contextlib import suppress
from typing import TYPE_CHECKING, TypedDict

import django
from django.db import OperationalError
from django.db.models import Count, F, Sum
from django_cte import CTEQuerySet, With

if TYPE_CHECKING:
    from django.db.models.query import _QuerySet
    from django_stubs_ext import WithAnnotations

django.setup()

from myapp.models import Order, Region  # noqa: E402


class RegionInfo(TypedDict):
    """Annotation of a region."""

    name: str


class RegionCounts(TypedDict):
    """Annotation of a region."""

    orders_count: int
    region_total: int


def make_root_mapping(rootmap: "With[Region]") -> "_QuerySet[Region, RegionInfo]":
    """Create the recursion CTE."""
    return (
        Region.objects.filter(
            parent__isnull=True,
        )
        .values(
            "name",
            root=F("name"),
        )
        .union(
            rootmap.join(Region, parent=rootmap.col.name).values(
                "name",
                root=rootmap.col.root,
            ),
            all=True,
        )
    )


rootmap: "With[Region]" = With.recursive(make_root_mapping, name="rootmap")

with suppress(OperationalError):
    wrong: int = rootmap.queryset().get()  # type: ignore[assignment]
    ok: "Region" = rootmap.queryset().get()
    ok_2: str = rootmap.queryset().get().name
    wrong_2: "Region" = rootmap.queryset().get().name  # type: ignore[assignment]

totals: "With[WithAnnotations[Region, RegionCounts]]" = With(
    rootmap.join(Order, region_id=rootmap.col.name)
    .values(
        root=rootmap.col.root,
    )
    .annotate(
        orders_count=Count("id"),
        region_total=Sum("amount"),
    ),
    name="totals",
)

with suppress(OperationalError):
    wrong_totals: int = totals.queryset().get()  # type: ignore[assignment]
    ok_totals: "Region" = totals.queryset().get()
    ok_2_totals: str = totals.queryset().get().name
    wrong_2_totals: "Region" = totals.queryset().get().name  # type: ignore[assignment]
    ok_3_totals: int = totals.queryset().get().orders_count
    wrong_3_totals: "Region" = totals.queryset().get().orders_count  # type: ignore[assignment]


root_regions: "CTEQuerySet[WithAnnotations[Region, RegionCounts]]" = (
    totals.join(Region, name=totals.col.root)
    # Important: add both CTEs to the final query
    .with_cte(rootmap)
    .with_cte(totals)
    .annotate(
        # count of orders in this region and all subregions
        orders_count=totals.col.orders_count,
        # sum of order amounts in this region and all subregions
        region_total=totals.col.region_total,
    )
)

with suppress(OperationalError):
    wrong_root_regions: int = root_regions.get()  # type: ignore[assignment]
    ok_root_regions: "Region" = root_regions.get()
    ok_2_root_regions: str = root_regions.get().name
    wrong_2_root_regions: "Region" = root_regions.get().name  # type: ignore[assignment]
    ok_3_root_regions: int = root_regions.get().orders_count
    wrong_3_root_regions: "Region" = root_regions.get().orders_count  # type: ignore[assignment]
    wrong_4_root_regions: "Region" = root_regions.get().not_orders_count  # type: ignore[attr-defined]
