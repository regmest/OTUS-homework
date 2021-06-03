"""
Домашнее задание №2
Классы и модули
"""
from . import base, car, engine, exceptions, plane

"""
Про __all__ - https://docs.python.org/3/tutorial/modules.html#importing-from-a-package
if a package’s __init__.py code defines a list named __all__, 
it is taken to be the list of module names that should be 
imported when from package import * is encountered. 
При вызове from homework_02 import * будут импортированы только перечисленные в __all__ модули. 
"""

__all__ = [
    "base",
    "car",
    "engine",
    "exceptions",
    "plane",
]
