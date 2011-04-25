#
#  USED TO CONVERT PYTHON DICTIONARIES TO OBJECTS
#  so instead of writing  dict['something'] we can write dict.something
#
#  Usage:
#        >> dict = {'a': 1, 'b': 2}
#        >> o = Struct(dict)
#        >> o.a
#        returns 1
#

__all__ = ['Struct', ]

class Struct:
    def __init__(self, **entries):
        self.__dict__.update(entries)
