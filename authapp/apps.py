from django.apps import AppConfig


class AuthappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'authapp'

    def ready(self):
        import authapp.signals
        from .signals import setup_groups
        from django.db.models.signals import post_migrate
        post_migrate.connect(setup_groups, sender=self)
