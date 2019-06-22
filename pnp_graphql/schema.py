import graphene
from graphene_django import DjangoObjectType

from example_app.models import Book


class BookType(DjangoObjectType):
    class Meta:
        model = Book


class Query(graphene.ObjectType):
    books = graphene.Field(BookType, id=graphene.Int())

    def resolve_books(self, info, **kwargs):
        return Book.objects.all()


class Mutation(graphene.ObjectType):
    success = graphene.Boolean()


schema = graphene.Schema(query=Query, mutation=Mutation)
