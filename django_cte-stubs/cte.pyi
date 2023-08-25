from typing import Callable, Generic, TypeVar

from django.db.models import Manager, Model, Q
from django.db.models.query import QuerySet, _QuerySet
from django.db.models.sql import Query
from typing_extensions import Self

from .meta import CTEColumn, CTEColumns
from .query import CTEQuery

_T_co = TypeVar("_T_co", bound=Model, covariant=True)
_T2_co = TypeVar("_T2_co", bound=Model, covariant=True)
_Row_co = TypeVar("_Row_co", covariant=True)
_Q_co = TypeVar("_Q_co", bound=_QuerySet, covariant=True)
_Q2_co = TypeVar("_Q2_co", bound=_QuerySet, covariant=True)


class With(Generic[_T_co]):
    query: CTEQuery
    name: str
    col: CTEColumns
    materialized: bool

    def __init__(self, queryset: _QuerySet[_T_co, _Row_co], name: str = ..., materialized: bool = ...) -> None: ...

    @classmethod
    def recursive(cls, make_cte_queryset: Callable[[With[_T_co]], _QuerySet[_T2_co, _Row_co]], name: str = ...,
                  materialized: bool = ...) -> With[_T2_co]: ...

    def join(self, model_or_queryset: _QuerySet[_T_co, _Row_co] | type[Model], *filter_q: Q,
             **filter_kw: CTEColumn) -> CTEQuerySet[_T_co]: ...

    def queryset(self) -> CTEQuerySet[_T_co]: ...


class ManagedWith(With[_T_co], Generic[_T_co, _Q_co]):
    query: CTEQuery
    name: str
    col: CTEColumns
    materialized: bool

    def __init__(self, queryset: _Q_co, name: str = ..., materialized: bool = ...) -> None: ...

    @classmethod
    def recursive(cls, make_cte_queryset: Callable[[ManagedWith[_T_co, _Q_co]], _Q2_co], name: str = ...,
                  materialized: bool = ...) -> ManagedWith[_T2_co, _Q2_co]: ...

    def join(self, model_or_queryset: _Q_co | type[Model], *filter_q: Q,  # type: ignore[override]
             **filter_kw: CTEColumn) -> ManagedCTEQuerySet[_T_co, _Q_co]: ...

    def queryset(self) -> ManagedCTEQuerySet[_T_co, _Q_co]: ...

class CTEQuerySet(QuerySet[_T_co], Generic[_T_co]):
    def __init__(self, model: type[Model] | None = ..., query: Query | None = ...,
                 using: str | None = ..., hints: dict[str, Model] | None = ...) -> None: ...

    def with_cte(self, cte: With) -> CTEQuerySet[_T_co]: ...

    @classmethod
    def as_manager(cls) -> CTEManager[_T_co]: ...


class ManagedCTEQuerySet(CTEQuerySet[_T_co], Generic[_T_co, _Q_co]):
    def __init__(self, model: type[Model] | None = ..., query: Query | None = ...,
                 using: str | None = ..., hints: dict[str, Model] | None = ...) -> None: ...

    def with_cte(self, cte: ManagedWith) -> _Q_co: ...  # type: ignore[override]

    @classmethod
    def as_manager(cls) -> CTEManager[_T_co]: ...


class CTEManager(Manager[_T_co]):
    @classmethod
    def from_queryset(cls, queryset_class: type[_QuerySet[_T_co, _T_co]], class_name: str | None = ...) -> type[
        Self]: ...
