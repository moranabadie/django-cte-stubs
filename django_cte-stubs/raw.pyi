from collections.abc import Mapping, Sequence
from typing import Any

from django.db.models import Field, Model, QuerySet
from typing_extensions import TypeVar

class RawCteSqlModel(Model): ...

# Lets callers declare the CTE columns by annotating the result with a RawCteSqlModel subclass
_T_RawCteSqlModel = TypeVar("_T_RawCteSqlModel", bound=RawCteSqlModel, default=RawCteSqlModel)

def raw_cte_sql(sql: str, params: Sequence[Any], refs: Mapping[str, Field[Any, Any]]) -> QuerySet[_T_RawCteSqlModel]: ...
