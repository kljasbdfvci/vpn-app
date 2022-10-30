from django.apps import AppConfig



class ActionConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'superclient.action'

    def ready(self):
        print("Init Tasks...")
        from superclient.action.task import service_checker
        service_checker(repeat=5)
