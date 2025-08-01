from typing import Any, Callable, Generic, Literal, TypeVar, overload

from django.db.models import Manager, Model
from django.db.models.query import QuerySet, _QuerySet
from django.db.models.sql import Query
from mypy.nodes import Expression
from typing_extensions import Self

from .meta import CTEColumns
from .query import CTEQuery

_T_co = TypeVar("_T_co", bound=Model, covariant=True)
_T2_co = TypeVar("_T2_co", bound=Model, covariant=True)
_Row_co = TypeVar("_Row_co", covariant=True)
_Q_co = TypeVar("_Q_co", bound=_QuerySet, covariant=True)
_SelectT = TypeVar("_SelectT", bound=Model | QuerySet | CTE)
_QuerySet_Var = TypeVar("_QuerySet_Var", bound=QuerySet)
_QuerySet2_Var = TypeVar("_QuerySet2_Var", bound=QuerySet)

def with_cte(*ctes: CTE[Any], select: _SelectT) -> _SelectT: ...

class CTE(Generic[_QuerySet_Var]):
    query: CTEQuery
    name: str
    col: CTEColumns
    materialized: bool

    def __init__(self, queryset: _QuerySet_Var | None, name: str = ..., materialized: bool = ...) -> None: ...
    def __getstate__(self) -> tuple[CTEQuery | None, str, bool]: ...
    def __setstate__(self, state: tuple[CTEQuery | None, str, bool]) -> None: ...
    @classmethod
    def recursive(
        cls,
        make_cte_queryset: Callable[[Self], _QuerySet[_T2_co, _Row_co]],
        name: str = ...,
        materialized: bool = ...,
    ) -> Self: ...
    @overload
    def join(
        self,
        model_or_queryset: _QuerySet2_Var,
        *filter_q: Any,
        _join_type: Literal["INNER JOIN", "LEFT OUTER JOIN"] | None = ...,
        **filter_kw: Any,
    ) -> _QuerySet2_Var: ...
    @overload
    def join(
        self,
        model_or_queryset: type[_T2_co],
        *filter_q: Any,
        _join_type: Literal["INNER JOIN", "LEFT OUTER JOIN"] | None = ...,
        **filter_kw: Any,
    ) -> QuerySet[_T2_co]: ...
    def queryset(self) -> _QuerySet_Var: ...
    def _resolve_ref(self, name: str) -> Expression: ...
    def resolve_expression(
        self,
        query: Any | None = None,
        allow_joins: bool = True,
        reuse: set[str] | None = None,
        summarize: bool = False,
        for_save: bool = False,
    ) -> Self: ...

class CTEQuerySet(QuerySet[_T_co]):
    def __init__(
        self,
        model: type[Model] | None = ...,
        query: Query | None = ...,
        using: str | None = ...,
        hints: dict[str, Model] | None = ...,
    ) -> None: ...
    @classmethod
    def as_manager(cls) -> CTEManager[_T_co]: ...

class ManagedCTEQuerySet(CTEQuerySet[_T_co], Generic[_T_co, _Q_co]):
    def __init__(
        self,
        model: type[Model] | None = ...,
        query: Query | None = ...,
        using: str | None = ...,
        hints: dict[str, Model] | None = ...,
    ) -> None: ...
    @classmethod
    def as_manager(cls) -> CTEManager[_T_co]: ...

class CTEManager(Manager[_T_co]):
    @classmethod
    def from_queryset(cls, queryset_class: type[_QuerySet[_T_co, _T_co]], class_name: str | None = ...) -> type[Self]: ...
