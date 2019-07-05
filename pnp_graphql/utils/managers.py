from django.apps import apps
from django.conf import settings

from pnp_graphql.constants import SETTINGS_ENABLED_APPS, SETTINGS_CONFIG


def get_settings_for_app():
    _settings_config = getattr(settings, SETTINGS_CONFIG, None)
    if _settings_config is None:
        raise Exception('You must declare PNP_GRAPHQL config on settings.')
    return _settings_config


def get_enabled_app_models():
    _settings_config = get_settings_for_app()
    _enabled_apps = _settings_config.get(SETTINGS_ENABLED_APPS, None)

    if _enabled_apps is None:
        raise Exception('Expected ENABLED_APPS on settings config.')

    _models = []
    for _app in _enabled_apps:
        app_models = apps.get_app_config(_app).get_models()
        _models += [_m for _m in app_models]
    return _models
