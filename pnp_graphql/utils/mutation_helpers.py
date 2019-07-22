import graphene
from graphene import Mutation

from pnp_graphql.constants import MODEL_INPUT_ATTR, MODEL_TYPE_ATTR
from pnp_graphql.input_generator import GraphQlInputGenerator
from pnp_graphql.utils.class_factory import class_factory
from pnp_graphql.utils.managers import get_model_fields, get_enabled_app_models


def prepare_mutate(model, _mutation_class, **kwargs):
    @staticmethod
    def mutate(root, info, input=None):
        _fields = get_model_fields(model=model, flat=True)
        _data = {}
        for f in _fields:
            if getattr(input, f, None):
                _data[f] = getattr(input, f)
        instance = model(**_data)
        instance.save()
        _mutation_params = {
            model.__name__.lower(): instance
        }
        return _mutation_class(**_mutation_params)

    return mutate


def prepare_mutation_class_attributes(model):
    _input_type = getattr(model, MODEL_INPUT_ATTR, None)
    _query_type = getattr(model, MODEL_TYPE_ATTR, None)
    _mutation_class_attrs = {
        'Arguments': class_factory(__class_name='Arguments', base_classes=(), input=_input_type()),
        model.__name__.lower(): graphene.Field(_query_type),
        'mutate': prepare_mutate(model=model, _mutation_class=Mutation)
    }
    return _mutation_class_attrs


def prepare_mutation_classes():
    _models = get_enabled_app_models()
    GraphQlInputGenerator.generate_input_types()
    _classes = []
    for m in _models:
        _attrs = prepare_mutation_class_attributes(model=m)
        # Creating a fake base class for making mutate properly.
        _base_class = class_factory(__class_name='Create' + m.__name__, base_classes=(Mutation,), **_attrs)
        _attrs.update(mutate=prepare_mutate(model=m, _mutation_class=_base_class))
        _class = class_factory(__class_name='Create' + m.__name__, base_classes=(_base_class,), **_attrs)
        _classes.append(_class)
    return tuple(_classes)
