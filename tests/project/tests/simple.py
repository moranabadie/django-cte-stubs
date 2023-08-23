from django.db.models import Sum, Manager
from django_cte import With, CTEQuerySet, CTEManager

import django
from django_cte.join import QJoin

django.setup()


from myapp.models import Book

cte = With(
    Book.objects
    .values("author_id")
    .annotate(total=Sum("nb_line"))
)
print(type(cte.queryset()))
print(type(cte.queryset().as_manager()))
print(isinstance(cte.queryset().as_manager(), CTEManager))
print(isinstance(Manager.from_queryset(CTEQuerySet), CTEManager))

orders = (
    # FROM orders INNER JOIN cte ON orders.region_id = cte.region_id
    cte.join(Book, author=cte.col.author_id)

    # Add `WITH ...` before `SELECT ... FROM orders ...`
    .with_cte(cte)

    # Annotate each Order with a "region_total"
    .annotate(author_total=cte.col.total)
)

print(orders.query)  # print SQL
from django.db.models.sql.constants import INNER
print(hash(1))

print(QJoin("d", 'd', 'd', "er").identity)
print(isinstance(QJoin("d", 'd', 'd', "er").__hash__(), int))