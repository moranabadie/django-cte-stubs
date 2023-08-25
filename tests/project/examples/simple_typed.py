"""Some simple checks."""
from typing import TypedDict

import django
from django.db.models import Sum
from django_cte import CTEQuerySet, With
from django_stubs_ext import WithAnnotations

django.setup()
from myapp.models import Order, Region  # noqa: E402

Order.objects.all().delete()
Region.objects.all().delete()
region = Region.objects.create(name="example")
Order.objects.create(amount=2, region=region)


class TypedRegionTotal(TypedDict):
    """The Region annotation."""

    region_total: int


cte: "With[Order]" = With(
    Order.objects
    .values("region_id")
    .annotate(total=Sum("amount")),
)

orders: CTEQuerySet[WithAnnotations[Order, TypedRegionTotal]] = (
    # FROM orders INNER JOIN cte ON orders.region_id = cte.region_id
    cte.join(Order, region=cte.col.region_id)

    # Add `WITH ...` before `SELECT ... FROM orders ...`
    .with_cte(cte)

    # Annotate each Order with a "region_total"
    .annotate(region_total=cte.col.total)
)


order: Order = orders.get()
assert isinstance(order, Order)

region_total: int = orders.get().region_total
assert isinstance(region_total, int)

mypy_raises: str = orders.get().region_total  # type: ignore[assignment]
