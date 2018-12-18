import os
from common.BaseSetupDown_new import UpDown


class Path:
    def __init__(self, path):
        self.path = os.path.abspath(os.path.join(os.path.dirname(__file__), path))

    def __str__(self):
        return '%s' % (self.path)


class ModuleMetaclass(type):
    """
    创建模块类的时候，自动添加用例方法
    eg：testLogin = Path(path)
    """

    def __new__(cls, name, bases, attrs):
        if name == 'Module':
            return type.__new__(cls, name, bases, attrs)
        print('Found Module: %s' % name)
        mappings = dict()
        for k, v in attrs.items():
            if isinstance(v, Path):
                print('Found mapping: %s ==> %s' % (k, v))
                mappings[k] = v
        for k in mappings.keys():
            print('caseMethod: %s' % k)
            attrs[k] = lambda self, value=attrs.pop(k): self.template(k, value)
        return type.__new__(cls, name, bases, attrs)


class Module(UpDown, metaclass=ModuleMetaclass):
    pass
    # def __init__(self, **kwarg):
    #     super(Module, self).__init__(**kwarg)
    #
    # def __getattr__(self, key):
    #     try:
    #         return self[key]
    #     except KeyError:
    #         raise AttributeError("'Model' object has no attribute '%s'" % key)
    #
    # def __setattr__(self, key, value):
    #     self[key] = value
    #
    # def __setitem__(self, key, value):
    #     self.key = value

# class Login(Module):
#     pass

#     testLogin = Path('../yamls/home/t1.yaml')
#     testStatus = Path('../yamls/home/login.yaml')
