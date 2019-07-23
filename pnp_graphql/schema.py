import graphene

from pnp_graphql.utils.class_factory import class_factory
from pnp_graphql.mutations.create_mutations import prepare_mutation_classes
from pnp_graphql.utils.query_helpers import get_query_attributes

# Getting query attributes with mapping
_query_attrs = get_query_attributes()
# Making query class with proper format
_query = class_factory(__class_name='Query', base_classes=(graphene.ObjectType,), **_query_attrs)


# class Mutation(graphene.ObjectType):
#     success = graphene.Boolean()


_mutation_base_classes = prepare_mutation_classes()
_mutation_attrs = {}
for _c in _mutation_base_classes:
    _mutation_attrs[_c.__name__.lower()] = getattr(_c, 'Field')()
_mutation = class_factory(
    __class_name='Mutation', 
    base_classes=(graphene.ObjectType,),
    **_mutation_attrs
)

# This schema will be declared to settings
schema = graphene.Schema(query=_query, mutation=_mutation)
