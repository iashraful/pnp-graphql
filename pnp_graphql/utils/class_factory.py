class BaseClass(object):
    """
    This is just a prototype of class.
    """
    def __init__(self, classtype):
        self._type = classtype


def class_factory(__class_name, base_classes=(BaseClass,), **kwargs):
    """

    :param __class_name: Name of the class which will be created
    :param base_classes: a list or tuple of base classes.
    :param kwargs: Anything you want to set as attribute.
    :return: newly created class
    """
    if type(base_classes) not in [list, tuple]:
        raise ValueError('A list/tuple of classes are required.')

    new_class = type(__class_name, base_classes, kwargs)
    return new_class
