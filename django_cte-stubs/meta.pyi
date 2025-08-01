from collections.abc import Mapping
from typing import Any

from django.db.backends.base.base import BaseDatabaseWrapper
from django.db.models import Field, Model, QuerySet
from django.db.models.expressions import Expression
from django.db.models.sql.compiler import SQLCompiler
from typing_extensions import Self, TypeAlias, override

from .cte import CTE

_Param: TypeAlias = str | int
_Params: TypeAlias = list[_Param] | tuple[_Param, ...]
_AsSqlType: TypeAlias = tuple[str, _Params]

class CTEColumns:
    def __init__(self, cte: CTE[QuerySet[Model, Any]]) -> None: ...
    def __getattr__(self, name: str) -> CTEColumn: ...

class CTEColumn(Expression):
    table_alias: str
    name: str
    alias: str | None
    _cte: CTE[QuerySet[Model, Any]]
    _output_field: Field[Any, Any] | None

    def __init__(self, cte: CTE[QuerySet[Model, Any]], name: str, output_field: Field[Any, Any] | None = ...) -> None: ...
    @property
    def _ref(self) -> Expression: ...
    @property
    def target(self) -> Field[Any, Any]: ...
    @override
    def as_sql(self, compiler: SQLCompiler, connection: BaseDatabaseWrapper) -> _AsSqlType: ...
    @override
    def relabeled_clone(self, change_map: Mapping[str, str]) -> Self: ...

class CTEColumnRef(Expression):
    name: str
    cte_name: str
    _alias: str | None

    def __init__(self, name: str, cte_name: str, output_field: Field[Any, Any]) -> None: ...
    @override
    def resolve_expression(
        self,
        query: Any = ...,
        allow_joins: bool = ...,
        reuse: set[str] | None = ...,
        summarize: bool = ...,
        for_save: bool = ...,
    ) -> CTEColumnRef: ...
    @override
    def relabeled_clone(self, change_map: Mapping[str, str]) -> Self: ...
    @override
    def as_sql(self, compiler: SQLCompiler, connection: BaseDatabaseWrapper) -> _AsSqlType: ...
