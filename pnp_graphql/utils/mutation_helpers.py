import graphene

from pnp_graphql.constants import MODEL_INPUT_ATTR, MODEL_TYPE_ATTR
from pnp_graphql.utils.class_factory import class_factory
from pnp_graphql.utils.managers import get_model_fields, get_enabled_app_models


def prepare_mutate(_class, model, **kwargs):
    @staticmethod
    def mutate(root, info, input=None):
        success = True
        _fields = get_model_fields(model=model, flat=True)
        _data = {}
        for f in _fields:
            if hasattr(input, f):
                _data[f] = getattr(input, f)
        instance = model(**_data)
        instance.save()
        return _class(success=success, data=instance)


def prepare_mutation_class_attributes(model):
    _input_type = getattr(model, MODEL_INPUT_ATTR, None)
    _query_type = getattr(model, MODEL_TYPE_ATTR, None)
    _mutation_class_attrs = {
        'Meta': class_factory(__class_name='Arguments', base_classes=(), input=_input_type),
        'success': graphene.Boolean(),
        'data': graphene.Field(_query_type)
    }
    return _mutation_class_attrs


def prepare_mutation_classes():
    _models = get_enabled_app_models()
    _classes = []
    for m in _models:
        _attrs = prepare_mutation_class_attributes(model=m)
        _class = class_factory(__class_name=m.__name__ + '')
