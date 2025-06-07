from django.apps import AppConfig


class HiringConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "hiring"

    def ready(self):
        import hiring.signals
