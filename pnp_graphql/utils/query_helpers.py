import graphene

from pnp_graphql.constants import MODEL_TYPE_ATTR
from pnp_graphql.type_generator import GraphQlTypeGenerator
from pnp_graphql.utils.managers import get_enabled_app_models


def resolve_list_items(model, **kwargs):
    """
    The wrapper function just wrap inner function to operate with GraphQL.

    This resolver function will help graphql to know about list type. I mean it will return inner function and
    inner function return list data

    :param model: A django model
    :param kwargs: Anything. currently not using
    :return: return inner function.
    """
    def resolve_list(self, info, **kwargs):
        """
        This method will be called internally from graphql query schema generator.
        :param self: it just a self variable for class instance method.
        :param info: graphql extra info
        :param kwargs: Expecting first and offset will be there. But anything could be.
        :return: queryset
        """
        queryset = model.objects.all()
        _page_size = kwargs.get('first', None)
        _offset = kwargs.get('offset', 0)
        if _page_size is not None:
            queryset = queryset.order_by('id')[_offset:_offset + _page_size]
        return queryset

    return resolve_list


def resolve_object_item(model, **kwargs):
    """
    The wrapper function just wrap inner function to operate with GraphQL.

    This resolver function will help graphql to know about object/single field type. I mean it will return inner
     function and inner function return a single object. Data accessible via ID

    :param model: A django model
    :param kwargs: Anything. currently not using
    :return: return inner function.
    """
    def resolve_object(self, info, **kwargs):
        """
        This method will be called internally from graphql query schema generator.
        :param self: it just a self variable for class instance method.
        :param info: graphql extra info
        :param kwargs: Expecting ID will be there. But anything could be.
        :return: queryset
        """
        queryset = model.objects.get(id=kwargs.get('id', 0))
        return queryset

    return resolve_object


def _make_list_type_name(model):
    """
    LIST QUERY TYPE NAME

    We need query type name. For example when we will query from graphql client end, we will be writing
    model name with lower and list with underscore or camelcase
    :param model:
    :return: a string name of query
    """
    return model.__name__.lower() + '_list'


def _make_object_type_name(model):
    """
    SINGLE OBJECT QUERY TYPE NAME

    We need query type name. For example when we will query from graphql client end, we will be writing
    model name with lower and list with underscore or camelcase
    :param model:
    :return: a string name of query
    """
    return model.__name__.lower() + '_object'


def _make_list_query_type(model):
    """
    Making actual query type field
    :param model: django model
    :return: query type field field
    """
    _query_type = getattr(model, MODEL_TYPE_ATTR, None)
    if _query_type:
        _type = graphene.List(
            _query_type,
            first=graphene.Int(),
            offset=graphene.Int()
        )
        return _type


def _make_object_query_type(model):
    """
    Making actual query type field
    :param model: django model
    :return: query type field field
    """
    _query_type = getattr(model, MODEL_TYPE_ATTR, None)
    if _query_type:
        _type = graphene.Field(
            _query_type,
            id=graphene.Int()
        )
        return _type


def get_query_attributes():
    """
    This is for Query Class attributes. The game plan is making a query class dynamically using type() keyword.
    While a Query class will be initiated then we will passed the attributes there. So that graphql can understand
    the query types and resolvers
    :return:
    """
    GraphQlTypeGenerator.generate_query_types()
    _models = get_enabled_app_models()
    _attrs = {}
    for _m in _models:
        # Return List Items
        _attrs[_make_list_type_name(_m)] = _make_list_query_type(model=_m)
        _attrs['resolve_' + _make_list_type_name(_m)] = resolve_list_items(model=_m)

        # Return Single Object (Ex: id: 10)
        _attrs[_make_object_type_name(_m)] = _make_object_query_type(model=_m)
        _attrs['resolve_' + _make_object_type_name(_m)] = resolve_object_item(model=_m)
    return _attrs
