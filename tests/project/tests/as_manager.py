"""Test as manager.."""

from __future__ import annotations

from contextlib import suppress
from typing import TYPE_CHECKING

import django
from django_cte import With

django.setup()

from myapp.models import LargeOrdersQuerySet, Order  # noqa: E402

if TYPE_CHECKING:
    from django.db.models import QuerySet
    from django_cte.cte import ManagedWith


wrong_example: int = Order.large.example()  # type: ignore[assignment]
good_example: LargeOrdersQuerySet = Order.large.example()
good_example_2: QuerySet[Order] = Order.large.example()
good_example_3: QuerySet[Order] = Order.large.all().example()
wrong_example_2: int = Order.large.all().example()  # type: ignore[assignment]
wrong_all: int = Order.large.all()  # type: ignore[assignment]
good_all: LargeOrdersQuerySet = Order.large.all()
# calling get or first directly fails for no reason (django-stubs bug)
with suppress(Order.DoesNotExist):
    wrong_get: int = Order.large.all().get()  # type: ignore[assignment]
    ok_get: Order = Order.large.all().get()

wrong_first: int | None = Order.large.all().first()  # type: ignore[assignment]
ok_first: Order | None = Order.large.all().first()

cte: ManagedWith[Order, LargeOrdersQuerySet] = With(
    Order.large.values("amount"),
)

with suppress(Order.DoesNotExist):
    wrong_with_cte: int = cte.queryset().with_cte(cte).get()  # type: ignore[assignment]
    good_with_cte: Order = cte.queryset().with_cte(cte).get()

wrong_with_cte_2: int = cte.queryset().with_cte(cte).example()  # type: ignore[assignment]
good_with_cte_2: LargeOrdersQuerySet = cte.queryset().with_cte(cte).example()

cte2: With[Order] = With(
    Order.large.values("amount"),
)
wrong_cte2: int = cte2.queryset().with_cte(cte).get()  # type: ignore[assignment]
Good_cte2: Order = cte2.queryset().with_cte(cte).get()
