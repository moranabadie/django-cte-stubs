"""Example of using CTEs with joins in Django."""

from django.db.models import Sum
from django.db.models.sql.constants import LOUTER
from django_cte import CTE, with_cte
from myapp.models import Order

totals = CTE(Order.objects.values("region_id").annotate(total=Sum("amount")).filter(total__gt=100))
reveal_type(totals)  # noqa:F821

reveal_type(totals.join(Order, region=totals.col.region_id, _join_type=LOUTER))  # noqa:F821
reveal_type(totals.join(Order, region=totals.col.region_id, _join_type=LOUTER).annotate(region_total=totals.col.total))  # noqa:F821

orders = with_cte(
    totals,
    select=totals.join(Order, region=totals.col.region_id, _join_type=LOUTER).annotate(region_total=totals.col.total),
)
reveal_type(orders)  # noqa:F821

wrong = orders.get().not_region_total  # type: ignore[attr-defined]
reveal_type(orders.get().region_total)  # noqa: F821
