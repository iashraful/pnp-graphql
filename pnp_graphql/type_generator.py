from example_app.models import *
from .utils.class_factory import ClassFactory, TypedClassFactory

class GraphQlTypeGenerator(object):
    @classmethod
    def get_models_for_typing(self, *args, **kwargs):
        return [Book]

    @classmethod
    def generate_query_type(self, *args, **kwargs):
        _models = cls.get_models_for_typing(*args, **kwargs)
        for _m in _models:
            _class = TypedClassFactory('{0}Type'.format(_m.__name__), model=_m)
