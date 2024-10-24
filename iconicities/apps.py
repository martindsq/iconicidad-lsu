from django.apps import AppConfig
from .options import IconicitiesOptions
from django.utils.translation import gettext_lazy as _

class IconicitiesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'iconicities'
    options = IconicitiesOptions()
    verbose_name = _('Iconicities')
