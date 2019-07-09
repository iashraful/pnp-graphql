from graphene_django import DjangoObjectType

from pnp_graphql.constants import MODEL_TYPE_ATTR
from pnp_graphql.utils.class_factory import class_factory
from pnp_graphql.utils.managers import get_enabled_app_models


class GraphQlTypeGenerator(object):
    @classmethod
    def get_models_for_typing(cls, *args, **kwargs):
        """
        Look for models and return them in a list
        :param args:
        :param kwargs: Expecting any values. Still not using it
        :return: list of Django model
        """
        return get_enabled_app_models()

    @classmethod
    def generate_query_types(cls, *args, **kwargs):
        """
        This method has a great power of creating graphql type object
        :param args:
        :param kwargs:
        :return: it doesn't return anything. Rather than return it set type class as attribute to model
        """
        _models = cls.get_models_for_typing(*args, **kwargs)
        for _m in _models:
            _meta_class = class_factory(__class_name='Meta', model=_m)
            _class = class_factory(
                __class_name='{0}Type'.format(_m.__name__), base_classes=(DjangoObjectType,), Meta=_meta_class)
            # Setting attribute to model. So that we can access from model
            setattr(_m, MODEL_TYPE_ATTR, _class)
