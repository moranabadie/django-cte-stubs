from typing import TypeVar, Generic, Callable

from django.db.models import Model, Q, Manager
from django.db.models.query import QuerySet
from django.db.models.sql import Query
from typing_extensions import Self

from .meta import CTEColumns

_T = TypeVar("_T", bound=Model, covariant=True)

class With(Generic[_T]):
    query: QuerySet[_T]
    name: str
    col: CTEColumns
    materialized: bool
    def __init__(self, queryset: QuerySet[_T], name: str = ..., materialized: bool = ...) -> None: ...
    @classmethod
    def recursive(cls, make_cte_queryset: Callable[[With[_T]], QuerySet[_T]], name: str = ..., materialized: bool = ...) -> With: ...
    def join(self, model_or_queryset: QuerySet[_T] | _T, *filter_q: Q, **filter_kw: QuerySet[_T] | _T) -> CTEQuerySet[_T]: ...
    def queryset(self) -> CTEQuerySet[_T]: ...

class CTEQuerySet(QuerySet[_T]):
    def __init__(self, model: type[Model] | None = ..., query: Query | None = ..., using: str | None = ..., hints: dict[str, Model] | None = ...) -> None: ...
    def with_cte(self, cte: With) -> CTEQuerySet[_T]: ...

    @classmethod
    def as_manager(cls) -> CTEManager[_T]: ...

class CTEManager(Manager[_T]):
    @classmethod
    def from_queryset(cls, queryset_class: type[QuerySet[_T]], class_name: str | None = ...) -> type[Self]: ...
