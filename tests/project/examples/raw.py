"""Raw sql."""

from typing import TypedDict

from django.db.models import IntegerField, QuerySet, TextField
from django_cte.cte import CTE, with_cte
from django_cte.raw import RawCteSqlModel, raw_cte_sql
from myapp.models import Region


class RawCTE(RawCteSqlModel):
    """The Typed Raw."""

    region_id = TextField()
    avg_order = IntegerField()


class Annotations(TypedDict):
    """The annotations."""

    avg_order: int


cte_sql: QuerySet[RawCTE] = raw_cte_sql(
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

reveal_type(cte_sql)  # noqa: F821


cte = CTE(cte_sql)
moon_avg = with_cte(cte, select=cte.join(Region, name=cte.col.region_id).annotate(avg_order=cte.col.avg_order))


annotated_raw = moon_avg.get()
reveal_type(annotated_raw)  # noqa: F821
wrong_avg_order: str = annotated_raw.avg_order  # type: ignore[assignment]

ok_avg_order: int = annotated_raw.avg_order
reveal_type(ok_avg_order)  # noqa: F821
