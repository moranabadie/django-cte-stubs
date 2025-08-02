from collections.abc import Mapping, Sequence
from typing import Any

from django.db.models import Field, Model, QuerySet

class RawCteSqlModel(Model): ...

def raw_cte_sql(sql: str, params: Sequence[Any], refs: Mapping[str, Field[Any, Any]]) -> QuerySet[RawCteSqlModel]: ...
