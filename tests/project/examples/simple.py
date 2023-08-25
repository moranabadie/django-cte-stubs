"""Some simple checks."""
import django
from django.db.models import Sum
from django_cte import With

django.setup()
from myapp.models import Order, Region  # noqa: E402

Order.objects.all().delete()
Region.objects.all().delete()
region = Region.objects.create(name="example")
Order.objects.create(amount=2, region=region)

cte = With(
    Order.objects
    .values("region_id")
    .annotate(total=Sum("amount")),
)

orders = (
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

# without strong typing of CTE, it can not know the type of region_total :
mypy_should_raise_but_it_does_not: str = orders.get().region_total
