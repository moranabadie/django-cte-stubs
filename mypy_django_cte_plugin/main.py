"""The entrypoint of the mypy plugin."""
from __future__ import annotations

from typing import TYPE_CHECKING, Callable

from mypy.plugin import FunctionContext, Plugin

if TYPE_CHECKING:
    from mypy.types import Type


class DjangoCtePluginPlugin(Plugin):
    """The django cte plugin."""

    def get_function_hook(self, fullname: str) -> Callable[[FunctionContext], Type] | None:
        """Manage when With is instantiated."""
        if fullname == "django_cte.cte.With":
            return check_managed_with_with_pattern
        return None


def check_managed_with_with_pattern(ctx: FunctionContext) -> Type:
    """Check if the expected type is ManagedWith, if yes, allow it."""
    for context in ctx.api.type_context:
        if context and "django_cte.cte.ManagedWith" in str(context):
            return context
    # If pattern doesn't match, return the default type inferred by mypy
    return ctx.default_return_type


def plugin(version: str) -> type[Plugin]:  # noqa: ARG001
    """Add the plugin."""
    return DjangoCtePluginPlugin
