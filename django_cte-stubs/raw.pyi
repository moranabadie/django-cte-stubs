from typing import TypeVar

from django.db.models import Field, Model
from django.db.models.query import QuerySet

class RawCteSqlModel(Model): ...


_T_RawCteSqlModel = TypeVar("_T_RawCteSqlModel", bound=RawCteSqlModel)

# it is not really true, but we are faking a Queryset.
def raw_cte_sql(sql: str, params: list[str], refs: dict[str, Field]) -> QuerySet[_T_RawCteSqlModel]: ...
