from django.utils.timezone import datetime, localdate, localtime, make_aware, timedelta
from django.apps import apps
from importlib import import_module


def aware_timedelta_days(to_move: datetime, timedelta_days: timedelta) -> datetime:
    # This is to check for correct timezone/DST setting, see why we separate date and time here:
    # https://gist.github.com/codeinthehole/1ac10da7874033406f25f86df07b88ff
    to_move_date = localdate(to_move) + timedelta_days
    to_move_time = localtime(to_move).time()

    return make_aware(datetime.combine(to_move_date, to_move_time))

def get_class_import_path(klass: type) -> str:
    module = klass.__module__
    qualname = klass.__qualname__
    if module == "builtins":
        return qualname
    return f"{module}.{qualname}"


class FormRegistry(object):
    """Register all subclasses of GDPRFormMixin to use in admin"""
    registry = {}

    def register(self, klass):
        import_path = get_class_import_path(klass)
        self.registry[import_path] = import_path

    def autodiscover(self):
        for app_config in apps.get_app_configs():
            try:
                import_module(f"{app_config.name}.forms")
            except Exception:
                pass

    def choices(self):
        """Return registry as choices"""
        return [(k, v) for k, v in self.registry.items()]

form_registry = FormRegistry()
