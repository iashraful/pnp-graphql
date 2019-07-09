from graphene import InputObjectType

from pnp_graphql.constants import MODEL_INPUT_ATTR
from pnp_graphql.utils.class_factory import class_factory
from pnp_graphql.utils.field_mappings import get_django_graphql_field_mapping
from pnp_graphql.utils.managers import get_enabled_app_models, get_model_fields


class GraphQlInputGenerator(object):
    """
    This class holds some set of methods for helping to create graphql input
    """
    @classmethod
    def generate_input_types(cls, *args, **kwargs):
        """
        This will generate input type and set them to model with specific attribute for future use
        :param args:
        :param kwargs:
        :return: nothing
        """
        # Get all models from the enabled app
        _models = get_enabled_app_models()
        # Pre declared field mapping
        _field_mapping = get_django_graphql_field_mapping()
        for m in _models:
            _input_type_dict = {}
            # Get all fields for model
            _fields = get_model_fields(model=m)
            for f in _fields:
                # Field is available at mapping
                if f[1] in _field_mapping.keys():
                    _input_type_dict[f[0]] = _field_mapping[f[1]]
            # Create input type class
            _class = class_factory(
                __class_name='{0}Input'.format(m.__name__), base_classes=(InputObjectType,),
                **_input_type_dict
            )
            # Setting the attribute to model
            setattr(m, MODEL_INPUT_ATTR, _class)
