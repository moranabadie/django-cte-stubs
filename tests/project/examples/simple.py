"""Some simple checks."""

from typing import reveal_type

import django
from django.db.models import Sum
from django_cte.cte import CTE, with_cte

django.setup()
from myapp.models import Order, Region  # noqa: E402

Order.objects.all().delete()
Region.objects.all().delete()
region = Region.objects.create(name="example")
Order.objects.create(amount=2, region=region)

cte = CTE(
    Order.objects.values("region_id").annotate(total=Sum("amount")),
)
reveal_type(cte)

orders = with_cte(
    # WITH cte ...
    cte,
    # SELECT ... FROM orders INNER JOIN cte ON orders.region_id = cte.region_id
    select=cte.join(Order, region=cte.col.region_id)
    # Annotate each Order with a "region_total"
    .annotate(region_total=cte.col.total),
)
reveal_type(orders)

order: Order = orders.get()
assert isinstance(order, Order)
reveal_type(order)

region_total: int = orders.get().region_total
assert isinstance(region_total, int)
reveal_type(region_total)

# without strong typing of CTE, it can not know the type of region_total :
mypy_should_raise_but_it_does_not: str = orders.get().region_total
