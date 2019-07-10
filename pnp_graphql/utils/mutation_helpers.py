import graphene
from graphene import Mutation

from pnp_graphql.constants import MODEL_INPUT_ATTR, MODEL_TYPE_ATTR
from pnp_graphql.utils.class_factory import class_factory
from pnp_graphql.utils.managers import get_model_fields, get_enabled_app_models
from pnp_graphql.input_generator import GraphQlInputGenerator


def prepare_mutate(model, **kwargs):
    @staticmethod
    def mutate(root, info, input=None):
        _fields = get_model_fields(model=model, flat=True)
        _data = {}
        for f in _fields:
            if hasattr(input, f):
                _data[f] = getattr(input, f)
        instance = model(**_data)
        instance.save()
        return Mutation(data=instance)
    return mutate


def prepare_mutation_class_attributes(model):
    _input_type = getattr(model, MODEL_INPUT_ATTR, None)
    _query_type = getattr(model, MODEL_TYPE_ATTR, None)
    _mutation_class_attrs = {
        'Arguments': class_factory(__class_name='Arguments', base_classes=(), input=_input_type()),
        'data': graphene.Field(_query_type),
        'mutate': prepare_mutate(model)
    }
    return _mutation_class_attrs


def prepare_mutation_classes():
    _models = get_enabled_app_models()
    GraphQlInputGenerator.generate_input_types()
    _classes = []
    for m in _models:
        _attrs = prepare_mutation_class_attributes(model=m)
        _class = class_factory(__class_name=m.__name__ + 'Create', base_classes=(Mutation,), **_attrs)
        _classes.append(_class)
    return tuple(_classes)
