from django.apps import AppConfig


class TrainerConfig(AppConfig):
    name = 'trainer'

    def ready(self):
        import trainer.signals  # noqa
