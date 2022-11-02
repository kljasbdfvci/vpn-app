from django.apps import AppConfig



class ActionConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'superclient.action'

    def ready(self):
        unregister_admin()

        if db_table_exists('background_task'):
            print("Init Tasks...")
            from superclient.action.task import service_checker
            service_checker(repeat=5)
            from superclient.action.task import quota
            quota(repeat=300)


def unregister_admin():
    from django.contrib import admin
    from django.contrib.auth.models import Group
    from background_task.models import CompletedTask, Task
    
    admin.site.unregister(Group)
    admin.site.unregister(CompletedTask)
    admin.site.unregister(Task)


def db_table_exists(table, cursor=None):
    try:
        if not cursor:
            from django.db import connection
            cursor = connection.cursor()
        if not cursor:
            raise Exception
        table_names = connection.introspection.get_table_list(cursor)
        table_names = [table.name for table in table_names]
    except:
        raise Exception("unable to determine if the table '%s' exists" % table)
    else:
        return table in table_names