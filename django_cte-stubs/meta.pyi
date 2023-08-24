from typing import Any

from django.db.backends.base.base import BaseDatabaseWrapper
from django.db.models import Field
from django.db.models.expressions import Expression
from django.db.models.sql.compiler import SQLCompiler, _AsSqlType
from typing_extensions import Self

from .cte import With

class CTEColumns:
    def __init__(self, cte: With) -> None: ...
    def __getattr__(self, name: str) -> CTEColumn: ...

class CTEColumn(Expression):
    table_alias: str
    name: str
    def __init__(self, cte: With, name: str, output_field: Field | None = ...) -> None: ...
    @property
    def target(self) -> Field: ...
    @property
    def output_field(self) -> Field: ...
    def as_sql(self, compiler: SQLCompiler, connection: BaseDatabaseWrapper) -> _AsSqlType: ...
    def relabeled_clone(self, relabels: dict[str | None, str]) -> CTEColumn: ...

class CTEColumnRef(Expression):
    name: str
    cte_name: str
    output_field: Field
    def __init__(self, name: str, cte_name: str, output_field: Field) -> None: ...

    def resolve_expression(
            self,
            query: Any = ...,  # noqa: ANN401
            allow_joins: bool = ...,
            reuse: set[str] | None = ...,
            summarize: bool = ...,
            for_save: bool = ...,
    ) -> CTEColumnRef: ...
    def relabeled_clone(self, change_map: dict[str | None, str]) -> Self: ...
    def as_sql(self, compiler: SQLCompiler, connection: BaseDatabaseWrapper) -> _AsSqlType: ...
