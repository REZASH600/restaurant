from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _

class BranchesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.branches'
    verbose_name = _("Branche")
    verbose_name_plural = _("Branches")
