from django.apps import AppConfig


class CustomAdminConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'custom_admin'
    verbose_name = 'Administration Personnalisée'
    
    def ready(self):
        import custom_admin.models  # Import signals
