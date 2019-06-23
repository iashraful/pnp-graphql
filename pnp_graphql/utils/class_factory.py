from graphql import GraphQLObjectType

class BaseClass(object):
    def __init__(self, classtype):
        self._type = classtype

def ClassFactory(name, BaseClass=BaseClass):
    def __init__(self, **kwargs):
        self._kwargs = kwargs
        BaseClass.__init__(self, name[:-len("Class")])
    new_class = type(name, (BaseClass,),{"__init__": __init__})
    return new_class


def TypedClassFactory(name, BaseClass=GraphQLObjectType):
    def __init__(self, **kwargs):
        self._kwargs = kwargs
        BaseClass.__init__(self, name[:-len("Class")])
    new_class = type(name, (BaseClass,),{"__init__": __init__})
    return new_class