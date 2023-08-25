"""The dummy app."""
from django.apps import AppConfig


class MyappConfig(AppConfig):
    """The dummy app."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "myapp"
