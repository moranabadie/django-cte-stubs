from typing import Any, Callable

from django.db.backends.base.base import BaseDatabaseWrapper
from django.db.models import Model
from django.db.models.sql import DeleteQuery, Query, UpdateQuery
from django.db.models.sql.compiler import (
    SQLUpdateCompiler,
    _AsSqlType,
)
from django.db.models.sql.where import WhereNode

from .cte import CTE

class CTEQuery(Query):
    _jit_mixin_prefix: str
    _with_ctes: tuple
    def __init__(self, model: type[Model] | None, where: type[WhereNode] = ..., alias_cols: bool = ...) -> None: ...
    @property
    def combined_queries(self) -> tuple: ...
    @combined_queries.setter
    def combined_queries(self, queries: tuple) -> None: ...
    def resolve_expression(self, *args: Any, **kwargs: Any) -> CTEQuery: ...
    def get_compiler(self, *args: Any, **kwargs: Any) -> CTECompiler: ...
    def chain(self, klass: type[Query] | None = ...) -> CTEQuery: ...

def generate_cte_sql(connection: BaseDatabaseWrapper, query: Query, as_sql: Callable) -> tuple[str, tuple]: ...
def get_cte_query_template(cte: CTE) -> str: ...
def _ignore_with_col_aliases(cte_query: Query) -> None: ...

class CTECompiler:
    _jit_mixin_prefix: str
    def as_sql(self, *args: Any, **kwargs: Any) -> _AsSqlType: ...

class NoAliasQuery:
    _jit_mixin_prefix: str
    def get_compiler(self, *args: Any, **kwargs: Any) -> NoAliasCompiler: ...

class NoAliasCompiler:
    _jit_mixin_prefix: str
    def get_select(self, *, with_col_aliases: bool = False, **kw: Any) -> Any: ...

class CTEUpdateQuery(UpdateQuery, CTEQuery): ...
class CTEDeleteQuery(DeleteQuery, CTEQuery): ...

QUERY_TYPES: dict[type[Query], type[CTEQuery]]

COMPILER_TYPES: dict[type[CTEQuery], type[SQLUpdateCompiler]]
