"""
Example with a custom QuerySet using CTEs in Django.

Thank you https://github.com/karolyi.
"""

from __future__ import annotations

from functools import cached_property
from typing import TYPE_CHECKING

from django.db.models import QuerySet
from django_cte import CTE, with_cte
from myapp.models import Region
from typing_extensions import Self


class CategoryQuerySet(QuerySet[Region]):
    def _get_parents_cte(self, cte_in: CTE[CategoryQuerySet]) -> Self:
        join_answer = cte_in.join(
            model_or_queryset=Region.objects.only("pk"),
            pk=cte_in.col.parent_id,
        ).only("parent")
        reveal_type(join_answer)  # noqa: F821
        answer = self.only("parent").union(join_answer)
        reveal_type(answer)  # noqa: F821
        return answer

    @cached_property
    def bulk_parents(self) -> dict[int, Region]:
        cte = CTE.recursive(make_cte_queryset=self._get_parents_cte)
        reveal_type(cte)  # noqa: F821

        _with_typing: CTE[CategoryQuerySet] = CTE.recursive(make_cte_queryset=self._get_parents_cte)

        reveal_type(cte.join(model_or_queryset=Region, pk=cte.col.parent_id))  # noqa: F821

        categories = with_cte(cte, select=cte.join(model_or_queryset=Region, pk=cte.col.parent_id))
        reveal_type(categories)  # noqa: F821
        answer = categories.distinct().in_bulk()
        reveal_type(answer)  # noqa: F821
        return answer

    def with_parents(self) -> Self:
        return self.all()


class RegionQuerySet(QuerySet[Region]):
    def _get_parents_cte(self, cte_in: CTE[RegionQuerySet]) -> Self:
        # The 'anchor' part is basically self, no need for an extra
        # `pk__in` filter
        qs_pk = Region.objects.only("pk")
        return self.only("parent").union(
            cte_in.join(model_or_queryset=qs_pk, pk=cte_in.col.parent_id).only("parent"),
        )

    @cached_property
    def bulk_parents(self) -> dict[int, Region]:
        if TYPE_CHECKING:
            cte_r = CTE[RegionQuerySet].recursive
        else:
            cte_r = CTE.recursive
        cte = cte_r(make_cte_queryset=self._get_parents_cte)
        categories = with_cte(cte, select=cte.join(model_or_queryset=Region, pk=cte.col.parent_id))
        return categories.distinct().in_bulk()
