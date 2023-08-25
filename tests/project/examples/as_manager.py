"""Example with as manager : see the models for more info."""
from typing import TYPE_CHECKING

import django
from django_cte.cte import With

django.setup()

from myapp.models import LargeOrdersQuerySet, Order, Region  # noqa: E402

if TYPE_CHECKING:
    from django_cte.cte import ManagedWith

Order.objects.all().delete()
Region.objects.all().delete()
region = Region.objects.create(name="example")
Order.objects.create(amount=2, region=region)

order_query: LargeOrdersQuerySet = Order.large.example()
assert isinstance(order_query, LargeOrdersQuerySet)

cte: "ManagedWith[Order, LargeOrdersQuerySet]" = With(
    Order.large.all(),
)

cte_query: LargeOrdersQuerySet = cte.queryset().with_cte(cte)

order: Order = cte_query.get()
assert isinstance(order, Order)

order_cte_query: LargeOrdersQuerySet = cte_query.example()
assert isinstance(order_cte_query, LargeOrdersQuerySet)
