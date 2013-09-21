#
# Captures the known primitives
#

class PrimitivesNotFound(Exception): pass

def _is_primitives_class(e):
    "NOT_RPYTHON"
    from som.primitives.primitives import Primitives
    import inspect
    _, entry = e
    return (inspect.isclass(entry) and
            issubclass(entry, Primitives)
            and entry is not Primitives)

def _setup_primitives():
    "NOT_RPYTHON"
    from importlib import import_module
    import inspect
    import py
    from pprint import pformat
    directory = py.path.local(__file__).dirpath()
    files = filter(lambda ent: ent.basename.endswith("_primitives.py"),
                   directory.listdir())
    mods = map(lambda mod: import_module("som.primitives." + mod.purebasename),
               files)
    all_members = map(lambda module: inspect.getmembers(module),
                      mods)
    all_members = reduce(lambda all, each: all + each, all_members)
    all_prims = filter(_is_primitives_class, all_members)
    prim_pairs = map(lambda (name, cls):
                (name[:name.find("Primitives")], cls),
                all_prims)
    return dict(prim_pairs)

_primitives = _setup_primitives()

def primitives_for_class(cls):
    key = cls.get_name().get_string()
    res = _primitives.get(key, None)
    if res is None:
        raise PrimitivesNotFound
    return res