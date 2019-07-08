from django.apps import apps
from django.conf import settings

from pnp_graphql.constants import SETTINGS_ENABLED_APPS, SETTINGS_CONFIG


def get_settings_for_app():
    """
    Check the configuration available on settings.py and return the config dictionary
    :return: config on dictionary format
    """
    _settings_config = getattr(settings, SETTINGS_CONFIG, None)
    if _settings_config is None:
        raise Exception('You must declare PNP_GRAPHQL config on settings.')
    return _settings_config


def get_enabled_app_models():
    """
    Inside the settings there is a mandatory setting for app enabled settings. This method find the settings and
    findout the models on the app.
    :return: return list models
    """
    _settings_config = get_settings_for_app()
    _enabled_apps = _settings_config.get(SETTINGS_ENABLED_APPS, None)

    if _enabled_apps is None:
        raise Exception('Expected ENABLED_APPS on settings config.')

    _models = []
    for _app in _enabled_apps:
        app_models = apps.get_app_config(_app).get_models()
        _models += [_m for _m in app_models]
    return _models


def get_model_fields(model, flat=False):
    """
    Find all the fields on a django model
    :param model: A django models.Model subclass (django model)
    :param flat: boolean type value
    :return: list of model field if not flat else list of tuple of fields
    """
    if flat:
        return [f.name for f in model._meta.get_fields()]
    return [(f.name, f.get_internal_type()) for f in model._meta.get_fields()]
