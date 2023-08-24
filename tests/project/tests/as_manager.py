"""Test as manager.."""
from __future__ import annotations

from contextlib import suppress
from typing import TYPE_CHECKING

import django

django.setup()
from myapp.models import LargeOrdersQuerySet, Order  # noqa: E402

if TYPE_CHECKING:
    from django.db.models import QuerySet
    from django_cte import CTEQuerySet

wrong_example: int = Order.large.example()  # type: ignore[assignment]
good_example: LargeOrdersQuerySet = Order.large.example()
good_example_2: CTEQuerySet[Order] = Order.large.example()
good_example_3: QuerySet[Order] = Order.large.example()
wrong_all: int = Order.large.all()  # type: ignore[assignment]
good_all: LargeOrdersQuerySet = Order.large.all()
# calling get or first directly fails for no reason (django-stubs bug)
with suppress(Order.DoesNotExist):
    wrong_get: int = Order.large.all().get()  # type: ignore[assignment]
    ok_get: Order = Order.large.all().get()

wrong_first: int | None = Order.large.all().first()  # type: ignore[assignment]
ok_first: Order | None = Order.large.all().first()
