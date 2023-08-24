from typing import Literal

from django.db.backends.base.base import BaseDatabaseWrapper
from django.db.models.sql.compiler import SQLCompiler, _AsSqlType
from django.db.models.sql.where import WhereNode
from typing_extensions import Self

class QJoin:
    filtered_relation: None
    parent_alias: str
    table_name: str
    table_alias: str
    on_clause: WhereNode
    join_type: Literal["INNER JOIN", "LEFT OUTER JOIN"]
    nullable: bool

    def __init__(self, parent_alias: str, table_name: str, table_alias: str,
                 on_clause: WhereNode, join_type: Literal["INNER JOIN", "LEFT OUTER JOIN"] = ...,
                 nullable: bool | None = ...) -> None: ...

    @property
    def identity(self) -> type[QJoin]: ...

    def __hash__(self) -> int: ...

    def __eq__(self, other: object) -> bool: ...

    def equals(self, other: object) -> bool: ...

    def as_sql(self, compiler: SQLCompiler, connection: BaseDatabaseWrapper) -> _AsSqlType: ...

    def relabeled_clone(self, change_map: dict[str | None, str]) -> Self: ...

    class join_field:  # noqa: N801
        class related_model:  # noqa: N801
            class _meta:  # noqa: N801
                local_concrete_fields: tuple
