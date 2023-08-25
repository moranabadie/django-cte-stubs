"""Raw sql."""
from typing import TYPE_CHECKING, TypedDict

import django
from django.db.models import IntegerField, QuerySet, TextField
from django_cte import With
from django_cte.raw import raw_cte_sql

django.setup()

from myapp.models import Order, Region  # noqa: E402

if TYPE_CHECKING:
    from django_cte.raw import RawCteSqlModel
    from django_stubs_ext import WithAnnotations


    class RawCTE(RawCteSqlModel):
        """The Typed Raw."""

        region_id = TextField()
        avg_order = IntegerField()

    class Annotations(TypedDict):
        """The annotations."""

        avg_order: int


Order.objects.all().delete()
Region.objects.all().delete()
region = Region.objects.create(name="moon")
Order.objects.create(amount=2, region=region)

raw_query: "QuerySet[RawCTE]" = raw_cte_sql(
    """
    SELECT region_id, AVG(amount) AS avg_order
    FROM orders
    WHERE region_id = %s
    GROUP BY region_id
    """,
    ["moon"],
    {
        "region_id": TextField(),
        "avg_order": IntegerField(),
    },
)

cte: "With[RawCTE]" = With(raw_query)
moon_avg = (
    cte
    .join(Region, name=cte.col.region_id)
    .annotate(avg_order=cte.col.avg_order)
    .with_cte(cte)
)

annotated_raw: "WithAnnotations[RawCTE, Annotations]" = moon_avg.get()
wrong_avg_order: str = annotated_raw.avg_order  # type: ignore[assignment]
ok_avg_order: int = annotated_raw.avg_order

