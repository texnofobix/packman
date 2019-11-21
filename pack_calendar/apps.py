from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class PackCalendarConfig(AppConfig):
    name = 'pack_calendar'
    verbose_name = _('Calendar')
