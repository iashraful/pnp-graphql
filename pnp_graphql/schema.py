import graphene

from pnp_graphql.utils.query_helpers import get_query_attributes
from pnp_graphql.utils.class_factory import class_factory

# Getting query attributes with mapping
_query_attrs = get_query_attributes()
# Making query class with proper format
_query = class_factory(name='Query', base_classes=(graphene.ObjectType,), **_query_attrs)


class Mutation(graphene.ObjectType):
    success = graphene.Boolean()


# This schema will be declared to settings
schema = graphene.Schema(query=_query, mutation=Mutation)
