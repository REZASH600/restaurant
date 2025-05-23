from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _

class MenusConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.menus'
    verbose_name = _('Menu')
    verbose_name_plural = _('Menus')


    def ready(self):
         from . import signals
