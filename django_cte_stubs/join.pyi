from _typeshed import Incomplete
from typing import Literal

from django.db.models.sql.constants import INNER, LOUTER
from django.db.models.sql.where import WhereNode


class QJoin:
    filtered_relation: Incomplete
    parent_alias: str
    table_name: str
    table_alias: str
    on_clause: Incomplete
    join_type: Incomplete
    nullable: bool

    def __init__(self, parent_alias: str, table_name: str, table_alias: str,
                 on_clause: WhereNode, join_type: Literal['INNER JOIN', 'LEFT OUTER JOIN'] = ...,
                 nullable: bool | None = ...) -> None: ...

    @property
    def identity(self) -> type[QJoin]: ...

    def __hash__(self) -> int: ...

    def __eq__(self, other: QJoin) -> bool: ...

    def equals(self, other: QJoin) -> bool: ...

    def as_sql(self, compiler, connection): ...

    def relabeled_clone(self, change_map): ...

    class join_field:
        class related_model:
            class _meta:
                local_concrete_fields: Incomplete
