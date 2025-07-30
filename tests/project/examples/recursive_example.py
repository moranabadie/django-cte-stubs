"""An example with recursion."""

from typing import TYPE_CHECKING, TypedDict, reveal_type

from django.db.models import F, IntegerField, TextField, Value
from django.db.models.functions import Concat
from django_cte.cte import CTE, with_cte
from myapp.models import Region

if TYPE_CHECKING:
    from django.db.models.query import _QuerySet


class RegionInfo(TypedDict):
    """Annotation of a region."""

    name: str


def make_regions_cte(cte: CTE[Region]) -> "_QuerySet[Region, RegionInfo]":
    """Copy pasted from the documentation."""
    return (
        Region.objects.filter(parent__isnull=True)
        .values(
            "name",
            path=F("name"),
            depth=Value(0, output_field=IntegerField()),
        )
        .union(
            # recursive union: get descendants
            cte.join(Region, parent=cte.col.name).values(
                "name",
                path=Concat(
                    cte.col.path,
                    Value(" / "),
                    F("name"),
                    output_field=TextField(),
                ),
                depth=cte.col.depth + Value(1, output_field=IntegerField()),
            ),
            all=True,
        )
    )


cte = CTE.recursive(make_regions_cte)
reveal_type(cte)
regions = with_cte(
    cte,
    select=cte.join(Region, name=cte.col.name)
    .annotate(
        path=cte.col.path,
        depth=cte.col.depth,
    )
    .filter(depth=2)
    .order_by("path"),
)
reveal_type(regions)

r = regions.get()
path: str = r.path
reveal_type(path)

depth: str = r.depth
reveal_type(depth)

assert r.not_depth  # type: ignore[attr-defined]
