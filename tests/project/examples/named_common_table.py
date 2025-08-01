"""Example of using named common table expressions (CTEs) with Django and mypy."""

from typing import TypedDict

from django.db.models import F, QuerySet
from django.db.models.aggregates import Count, Sum
from django_cte.cte import CTE, with_cte
from myapp.models import Order, Region


class RootMapping(TypedDict):
    name: str
    root: str


def make_root_mapping(rootmap: CTE[QuerySet[Region, RootMapping]]) -> QuerySet[Region, RootMapping]:
    return (
        Region.objects.filter(parent__isnull=True)
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


rootmap = CTE.recursive(make_root_mapping, name="rootmap")
reveal_type(rootmap)  # noqa: F821

reveal_type(rootmap.join(Order, region_id=rootmap.col.name))  # noqa: F821

totals = CTE(
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

reveal_type(totals)  # noqa: F821

root_regions = with_cte(
    rootmap,
    totals,
    select=totals.join(Region, name=totals.col.root).annotate(
        # count of orders in this region and all subregions
        orders_count=totals.col.orders_count,
        # sum of order amounts in this region and all subregions
        region_total=totals.col.region_total,
    ),
)

reveal_type(root_regions)  # noqa: F821

reveal_type(root_regions.get().orders_count)  # noqa: F821
reveal_type(root_regions.get().region_total)  # noqa: F821

_ = root_regions.get().not_region_total  # type: ignore[attr-defined]
