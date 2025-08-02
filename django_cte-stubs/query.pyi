from typing import Any, Callable

from django.db.backends.base.base import BaseDatabaseWrapper
from django.db.models import Model, QuerySet
from django.db.models.sql import Query
from django.db.models.sql.compiler import (
    SQLUpdateCompiler,
)
from django.db.models.sql.where import WhereNode
from django_cte.jitmixin import JITMixin
from typing_extensions import TypeAlias, override

from .cte import CTE

_Param: TypeAlias = str | int
_Params: TypeAlias = list[_Param] | tuple[_Param, ...]
_AsSqlType: TypeAlias = tuple[str, _Params]

class CTEQuery(Query):
    _jit_mixin_prefix: str
    _with_ctes: tuple[Any, ...]
    def __init__(self, model: type[Model] | None, where: type[WhereNode] = ..., alias_cols: bool = ...) -> None: ...
    @override
    def resolve_expression(self, *args: Any, **kwargs: Any) -> CTEQuery: ...
    @override
    def get_compiler(self, *args: Any, **kwargs: Any) -> CTECompiler: ...
    @override
    def chain(self, klass: type[Query] | None = ...) -> CTEQuery: ...

def generate_cte_sql(
    connection: BaseDatabaseWrapper,
    query: Query,
    as_sql: Callable[[], tuple[str, tuple[Any, ...]]],
) -> tuple[str, tuple[Any, ...]]: ...
def get_cte_query_template(cte: CTE[QuerySet[Model, Any]]) -> str: ...
def _ignore_with_col_aliases(cte_query: Query) -> None: ...

class CTECompiler(JITMixin):
    _jit_mixin_prefix: str
    def as_sql(self, *args: Any, **kwargs: Any) -> _AsSqlType: ...

class NoAliasQuery(JITMixin):
    _jit_mixin_prefix: str
    def get_compiler(self, *args: Any, **kwargs: Any) -> NoAliasCompiler: ...

class NoAliasCompiler(JITMixin):
    _jit_mixin_prefix: str
    def get_select(self, *, with_col_aliases: bool = False, **kw: Any) -> Any: ...

QUERY_TYPES: dict[type[Query], type[CTEQuery]]

COMPILER_TYPES: dict[type[CTEQuery], type[SQLUpdateCompiler]]
