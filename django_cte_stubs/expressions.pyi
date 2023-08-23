from typing import Any

from django.db.models import Expression


class CTESubqueryResolver:
    annotation: Expression
    def __init__(self, annotation: Expression) -> None: ...
    def resolve_expression(
        self,
        query: Any = ...,
        allow_joins: bool = ...,
        reuse: set[str] | None = ...,
        summarize: bool = ...,
        for_save: bool = ...,
    ) -> CTESubqueryResolver: ...
