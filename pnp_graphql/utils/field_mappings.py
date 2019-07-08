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
