"""
    purplescript.compiler
    ~~~~~~~~~~~~

    :copyright: (c) 2010 by Martin Rusev.
    :license: BSD, see LICENSE for more details.
"""

__all__ = ['Compiler']

class Compiler(object):

    def __init__(self, output_file='test.php', template=None):
        print template
        with open(output_file, 'w+') as f:
             for line in template:
                 f.write(template[line])
                 f.write('\n')