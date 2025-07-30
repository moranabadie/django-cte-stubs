"""Raw sql."""

from contextlib import suppress
from typing import TYPE_CHECKING

import django
from django.db import OperationalError
from django.db.models import IntegerField, QuerySet, TextField
from django_cte import With
from django_cte.raw import raw_cte_sql

django.setup()

from myapp.models import Region  # noqa: E402

if TYPE_CHECKING:
    from django_cte.raw import RawCteSqlModel

    class RawCTE(RawCteSqlModel):
        """The Typed Raw."""

        region_id = TextField()
        avg_order = IntegerField()


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
moon_avg = cte.join(Region, name=cte.col.region_id).annotate(avg_order=cte.col.avg_order).with_cte(cte)

with suppress(OperationalError):
    wrong: int = moon_avg.get()  # type: ignore[assignment]
    ok: "RawCTE" = moon_avg.get()
    wrong_avg_order: str = ok.avg_order  # type: ignore[assignment]
    ok_avg_order: int = ok.avg_order
    wrong_region_id: int = ok.region_id  # type: ignore[assignment]
    ok_region_id: str = ok.region_id
