from django.apps import AppConfig

class SummariesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'summaries'

    def ready(self):
        import summaries.signals # Esta linha garante que o Django caregue os sinais