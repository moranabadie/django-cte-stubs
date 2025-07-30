from collections.abc import Mapping, Sequence
from typing import Any, TypeVar

from django.db.models import Field, Model, QuerySet

class RawCteSqlModel(Model): ...

_T_RawCteSqlModel = TypeVar("_T_RawCteSqlModel", bound=RawCteSqlModel)

def raw_cte_sql(sql: str, params: Sequence[Any], refs: Mapping[str, Field]) -> QuerySet[_T_RawCteSqlModel]: ...
