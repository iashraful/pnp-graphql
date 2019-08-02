import graphene
from graphene import Mutation

from pnp_graphql.constants import MODEL_INPUT_ATTR, MODEL_TYPE_ATTR
from pnp_graphql.utils.class_factory import class_factory
from pnp_graphql.utils.field_mappings import get_single_relation_fields, get_many_relation_fields
from pnp_graphql.utils.managers import get_model_fields, get_enabled_app_models, get_auth_class


def prepare_create_mutate(model, _mutation_class, **kwargs):
    """
    Preparing main mutation operations here. Basically here we will create the actual object.
    Child method will directly injected to mutation class. According to graphene documention it should be
    static method.
    :param model: Django model
    :param _mutation_class: future mutation class
    :param kwargs:
    :return: child method of muatation
    """

    @staticmethod
    def mutate(root, info, input=None):
        """
        Map the field with input fields and create
        :param root:
        :param info:
        :param input: input data.
        :return: mutate class ref object
        """
        auth_class = get_auth_class()
        if auth_class:
            auth_class().authenticate(info.context)
        _fields = get_model_fields(model=model, flat=False)
        _data = {}
        _m2m_data_mapping = []
        for f in _fields:
            if getattr(input, f[0], None):
                if f[1] in get_single_relation_fields():
                    _data[f[0] + '_id'] = getattr(input, f[0])
                elif f[1] in get_many_relation_fields():
                    _m2m_data_mapping.append(
                        (f[0], getattr(input, f[0]))
                    )
                else:
                    _data[f[0]] = getattr(input, f[0])
        instance = model(**_data)
        instance.save()
        for d in _m2m_data_mapping:
            if hasattr(instance, d[0]):
                getattr(instance, d[0]).add(*d[1])
        _mutation_params = {
            model.__name__.lower(): instance
        }
        return _mutation_class(**_mutation_params)

    return mutate


def prepare_create_mutation_class_attributes(model):
    """
    Preparing derived mutation class attributes. For example: Arguments is like meta class. So, I am including it here
    :param model: A django model
    :return: python dictionary of attributes
    """
    _input_type = getattr(model, MODEL_INPUT_ATTR, None)
    _query_type = getattr(model, MODEL_TYPE_ATTR, None)
    _mutation_class_attrs = {
        'Arguments': class_factory(
            __class_name='Arguments', base_classes=(),
            input=_input_type(required=True)
        ),
        model.__name__.lower(): graphene.Field(_query_type),
        'mutate': prepare_create_mutate(model=model, _mutation_class=Mutation)
    }
    return _mutation_class_attrs


def prepare_create_mutation_classes():
    """
    Here it's preparing actual mutation classes for each model.
    :return: A tuple of all mutation classes
    """
    _models = get_enabled_app_models()
    _classes = []
    for m in _models:
        _attrs = prepare_create_mutation_class_attributes(model=m)
        # Creating a fake base class for making mutate properly.
        _base_class = class_factory(__class_name='Create' + m.__name__, base_classes=(Mutation,), **_attrs)
        _attrs.update(mutate=prepare_create_mutate(model=m, _mutation_class=_base_class))
        _class = class_factory(__class_name='Create' + m.__name__, base_classes=(_base_class,), **_attrs)
        _classes.append(_class)
    return tuple(_classes)
