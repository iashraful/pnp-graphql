import graphene
from django.db import models


def get_django_graphql_field_mapping():
    """
    This method hold the field type mapping for query type with graphql.
    :return: a mapping dictionary
    """
    return {
        models.AutoField.__name__: graphene.Int(),
        models.BigAutoField.__name__: graphene.Int(),
        models.IntegerField.__name__: graphene.Int(),
        models.PositiveIntegerField.__name__: graphene.Int(),
        models.PositiveSmallIntegerField.__name__: graphene.Int(),
        models.SmallIntegerField.__name__: graphene.Int(),
        models.CharField.__name__: graphene.String(),
        models.TextField.__name__: graphene.String(),
        models.ForeignKey.__name__: graphene.Int(),
        models.OneToOneField.__name__: graphene.Int(),
        models.DateTimeField.__name__: graphene.DateTime(),
        models.DateField.__name__: graphene.Date(),
        models.ManyToManyField.__name__: graphene.List(of_type=graphene.Int),
    }


def get_filter_type_mapping():
    """
    This method holds the django filter type mapping.
    For Example: name search with `name__icontains="value"`
    :return: a dictionary mapping
    """
    return {
        models.AutoField.__name__: '',
        models.BigAutoField.__name__: '',
        models.IntegerField.__name__: '',
        models.PositiveIntegerField.__name__: '',
        models.PositiveSmallIntegerField.__name__: '',
        models.SmallIntegerField.__name__: '',
        models.CharField.__name__: '__icontains',
        models.TextField.__name__: '__icontains',
        models.ForeignKey.__name__: '',
        models.OneToOneField.__name__: '',
        models.DateTimeField.__name__: '__gte',
        models.DateField.__name__: '__gte',
    }


def get_single_relation_fields():
    """
    This method holds the django relational field type mapping
    :return: a list of fields
    """
    return [
        models.ForeignKey.__name__, models.OneToOneField.__name__
    ]


def get_many_relation_fields():
    """
    This method holds the django relational field type mapping
    :return: a list of fields
    """
    return [
        models.ManyToManyField.__name__,
    ]
