from django.apps import AppConfig


class BlogConfig:
    default_auto_field = "django.db.models.BigAutoField"
    name = "blog"

class CatalogConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "catalog"
