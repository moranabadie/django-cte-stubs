from typing import Any, Callable

from django.db.backends.base.base import BaseDatabaseWrapper
from django.db.models import Expression, Model
from django.db.models.sql import DeleteQuery, Query, UpdateQuery
from django.db.models.sql.compiler import (
    SQLCompiler,
    SQLDeleteCompiler,
    SQLUpdateCompiler,
    _AsSqlType,
)
from django.db.models.sql.where import WhereNode

from .cte import With
from .expressions import CTESubqueryResolver as CTESubqueryResolver

class CTEQuery(Query):
    def __init__(self, model: type[Model] | None, where: type[WhereNode] = ..., alias_cols: bool = ...) -> None: ...

    def combine(self, rhs: Query, connector: str) -> None: ...

    def get_compiler(self, using: str | None = ..., connection: BaseDatabaseWrapper | None = ...,
                     *args: Any, **kwargs: Any) -> SQLCompiler: ...   # noqa: ANN401

    def add_annotation(self, annotation: Expression, *args: Any, **kw: Any) -> None: ...  # noqa: ANN401

    def chain(self, klass: type[Query] | None = ...) -> Query: ...


class CTECompiler:
    @classmethod
    def generate_sql(cls, connection: BaseDatabaseWrapper, query: Query, as_sql: Callable) -> tuple[str, tuple]: ...

    @classmethod
    def get_cte_query_template(cls, cte: With) -> str: ...


class CTEUpdateQuery(UpdateQuery, CTEQuery): ...


class CTEDeleteQuery(DeleteQuery, CTEQuery): ...


QUERY_TYPES: dict[type[Query], type[CTEQuery]]


class CTEQueryCompiler(SQLCompiler):
    def as_sql(self, with_limits: bool = ..., with_col_aliases: bool = ...) -> _AsSqlType: ...


class CTEUpdateQueryCompiler(SQLUpdateCompiler):
    def as_sql(self, with_limits: bool = ..., with_col_aliases: bool = ...) -> _AsSqlType: ...


class CTEDeleteQueryCompiler(SQLDeleteCompiler):
    def as_sql(self, with_limits: bool = ..., with_col_aliases: bool = ...) -> _AsSqlType: ...


COMPILER_TYPES: dict[type[CTEQuery], type[SQLUpdateCompiler]]
