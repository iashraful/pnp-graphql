import graphene

from pnp_graphql.constants import MODEL_TYPE_ATTR
from pnp_graphql.type_generator import GraphQlTypeGenerator
from pnp_graphql.utils.class_factory import class_factory
from pnp_graphql.utils.managers import get_enabled_app_models


class Mutation(graphene.ObjectType):
    success = graphene.Boolean()


def resolve_list_items(model, **kwargs):
    def resolve_list(self, info, **kwargs):
        queryset = model.objects.all()
        _page_size = kwargs.get('first', None)
        _offset = kwargs.get('offset', 0)
        if _page_size is not None:
            queryset = queryset.order_by('id')[_offset:_offset + _page_size]
        return queryset

    return resolve_list


def resolve_object_item(model, **kwargs):
    def resolve_object(self, info, **kwargs):
        queryset = model.objects.get(id=kwargs.get('id', 0))
        return queryset

    return resolve_object


def _make_list_type_name(model):
    return model.__name__.lower() + '_list'


def _make_object_type_name(model):
    return model.__name__.lower() + '_object'


def _make_list_query_type(model):
    _query_type = getattr(model, MODEL_TYPE_ATTR, None)
    if _query_type:
        _type = graphene.List(
            _query_type,
            first=graphene.Int(),
            offset=graphene.Int()
        )
        return _type


def _make_object_query_type(model):
    _query_type = getattr(model, MODEL_TYPE_ATTR, None)
    if _query_type:
        _type = graphene.Field(
            _query_type,
            id=graphene.Int()
        )
        return _type


def get_query_attributes():
    _models = get_enabled_app_models()
    _attrs = {}
    for _m in _models:
        _attrs[_make_list_type_name(_m)] = _make_list_query_type(model=_m)
        _attrs['resolve_' + _make_list_type_name(_m)] = resolve_list_items(model=_m)
    return _attrs


GraphQlTypeGenerator.generate_query_types()
_query_attrs = get_query_attributes()
_query = class_factory(name='Query', base_classes=(graphene.ObjectType,), **_query_attrs)
schema = graphene.Schema(query=_query, mutation=Mutation)
